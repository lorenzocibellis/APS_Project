"""
=============================================================================
TEST DI SICUREZZA E SIMULAZIONE ATTACCHI
=============================================================================
Questo script verifica sperimentalmente la robustezza del sistema contro le
minacce formali definite nel Threat Model del Progetto:

1. Replay Attack sulla rete
2. Man-in-the-Middle e Manomissione dati
3. Accesso non autorizzato
4. Token di Autorizzazione Scaduto
5. Manomissione Registro di Audit
6. Clinica Disonesta / Aggiornamento Illecito
=============================================================================
"""

from datetime import datetime, timezone, timedelta
from cryptography.fernet import InvalidToken

from CentralSystem.data.database import Database
from CentralSystem.rm import RM
from thirdParties.ca import CA
from users.clinic import Clinica
from users.patient import Paziente
from users.medic import Medico
from globalClasses.enumerations import Role, OperationCode as oc, NotifyCode as nc
from cryptoOperation.cryptOp import S
from cryptoOperation.serializer import Serializer


def run_security_tests():

    print("=" * 65)

    ca = CA()
    db = Database()
    rm = RM(Role.RM, ca, db)
    clinica = Clinica(ca, rm)
    paziente = Paziente(ca, rm)
    medico = Medico(ca, rm)

    # caricamento referto di prova
    print("\n[*] Setup: Creazione e invio referto legittimo...")
    id_ref = clinica.createReferto(paziente._ID, "REF_SEC_TEST", "Parametri clinici")
    clinica.sendReferto(paziente._ID, id_ref)

    superati = 0
    totali = 6

    # -------------------------------------------------------------------------
    # TEST 1: REPLAY ATTACK
    # -------------------------------------------------------------------------
    print("\n" + "-" * 65)
    print("TEST 1: Attacco Replay")
    print("-" * 65)
    print("Simulazione: L'attaccante intercetta un pacchetto legittimo e prova")
    print("a re-inviarlo ad RM per replicare la richiesta senza un nuovo contatore.")

    packets_to_rm = []
    orig_send = ca._cc.send
    def spy_channel(dest, c):
        if dest == rm._ID:
            packets_to_rm.append(c)
        orig_send(dest, c)
    ca._cc.send = spy_channel

    paziente.ref_request(id_ref)
    captured_packet = packets_to_rm[-1]

    notifiche_rm = []
    orig_rm_notify = rm._notify
    rm._notify = lambda code: (notifiche_rm.append(code), orig_rm_notify(code))

    rm.receive(captured_packet)
    rm._notify = orig_rm_notify

    if notifiche_rm and notifiche_rm[-1] == nc.INVALID_DATA:
        print("-> ESITO: [SUPERATO] Bloccato con successo da RM (pacchetto replay rilevato e scartato)")
        superati += 1
    else:
        print("-> ESITO: [FALLITO] L'attacco Replay non è stato intercettato")

    ca._cc.send = orig_send

    # -------------------------------------------------------------------------
    # TEST 2: MAN-IN-THE-MIDDLE
    # -------------------------------------------------------------------------
    print("\n" + "-" * 65)
    print("TEST 2: Manomissione in transito")
    print("-" * 65)
    print("Simulazione: L'attaccante altera i byte del messaggio cifrato in transito.")

    c1, c2 = captured_packet
    tampered_packet = [c1, c2[:-10] + b"ATTACK_CORRUPT"]
    try:
        rm.receive(tampered_packet)
        print("-> ESITO: [FALLITO] Il messaggio manomesso è stato accettato")
    except (InvalidToken, Exception) as e:
        print(f"-> ESITO: [SUPERATO] Manomissione rilevata ({type(e).__name__}): pacchetto scartato")
        superati += 1

    # -------------------------------------------------------------------------
    # TEST 3: ACCESSO NON AUTORIZZATO
    # -------------------------------------------------------------------------
    print("\n" + "-" * 65)
    print("TEST 3: Accesso non autorizzato (Medico senza consenso del Paziente)")
    print("-" * 65)
    print("Simulazione: Un medico tenta di richiedere il referto a RM fornendo")
    print("un token di autorizzazione contraffatto (firma falsa).")

    medico_non_autorizzato = Medico(ca, rm)
    notifiche_m1 = []
    medico_non_autorizzato._notify = lambda code: notifiche_m1.append(code)

    auth_contraffatta = [
        b"FIRMA_FALSA_ATTACCANTE_12345",
        medico_non_autorizzato._ID,
        paziente._ID,
        id_ref,
        datetime.now(timezone.utc)
    ]
    richiesta_illecita = [medico_non_autorizzato._ID, oc.REF_REQ, paziente._ID, id_ref, auth_contraffatta]
    medico_non_autorizzato.send(rm._ID, richiesta_illecita)

    if notifiche_m1 and notifiche_m1[-1] == nc.UNAUTH:
        print("-> ESITO: [SUPERATO] RM ha verificato la firma del token e ha respinto la richiesta")
        superati += 1
    else:
        print("-> ESITO: [FALLITO] Accesso non autorizzato non gestito correttamente.")

    # -------------------------------------------------------------------------
    # TEST 4: TOKEN DI AUTORIZZAZIONE SCADUTO
    # -------------------------------------------------------------------------
    print("\n" + "-" * 65)
    print("TEST 4: Token di Autorizzazione Scaduto")
    print("-" * 65)
    print("Simulazione: Un medico presenta un token regolarmente firmato dal paziente,")
    print("ma emesso oltre il limite consentito di validità.")

    notifiche_m0 = []
    medico._notify = lambda code: notifiche_m0.append(code)

    data_scaduta = datetime.now(timezone.utc) - timedelta(days=40)
    auth_scaduta = [medico._ID, paziente._ID, id_ref, data_scaduta]
    firma_paziente = S.Sign(paziente._kpriv, Serializer.serialize(auth_scaduta))
    auth_scaduta.insert(0, firma_paziente)

    richiesta_scaduta = [medico._ID, oc.REF_REQ, paziente._ID, id_ref, auth_scaduta]
    medico.send(rm._ID, richiesta_scaduta)

    if notifiche_m0 and notifiche_m0[-1] == nc.UNAUTH:
        print("-> ESITO: [SUPERATO] RM ha controllato la data di emissione e ha respinto il token scaduto")
        superati += 1
    else:
        print("-> ESITO: [FALLITO] Token scaduto accettato")

    # -------------------------------------------------------------------------
    # TEST 5: MANOMISSIONE REGISTRO DI AUDIT
    # -------------------------------------------------------------------------
    print("\n" + "-" * 65)
    print("TEST 5: Integrità Registro di Audit")
    print("-" * 65)
    print("Simulazione: Un RM malevolo altera retroattivamente una voce di audit")
    print("(es. manomissione contatore) prima di consegnare il registro al client.")

    item = db.getItem(paziente._ID, id_ref)
    registro = item.getRegister()

    # manomissione del primo audit
    audit_0, hash_0 = registro.getAudit(0)
    vecchio_cnt = audit_0._cnt
    audit_0._cnt = 999999

    valid = paziente._verifyRegister(registro,paziente._ID, id_ref)
    # ripristino
    audit_0._cnt = vecchio_cnt

    if not valid:
        print("-> ESITO: [SUPERATO] Il client ha rilevato l'incoerenza crittografica dell'audit (firme/hash errati)")
        superati += 1
    else:
        print("-> ESITO: [FALLITO] Manomissione dell'audit non rilevata")

    # -------------------------------------------------------------------------
    # TEST 6: CLINICA DISONESTA - MODIFICA SENZA REVOCA
    # -------------------------------------------------------------------------
    print("\n" + "-" * 65)
    print("TEST 6: Aggiornamento senza previa Revoca")
    print("-" * 65)
    print("Simulazione: La clinica tenta di sovrascrivere direttamente un referto")
    print("attivo senza aver prima depositato la formale Motivazione di Revoca (MdR).")

    #simulazione di una clinica che invia un aggiornamento senza aver revocato un referto
    #impostiamo il bit di revoca a True anche se il referto è ancora valido
    clinica._database[paziente._ID][id_ref][0] = True

    told = rm._db.getItem(paziente._ID, id_ref)._trev
    clinica.updateReferto(paziente._ID, id_ref, "Referto modificato abusivamente")

    #Controllo che il token di validazione non sia modificato
    if told == rm._db.getItem(paziente._ID, id_ref)._trev:
        print("-> ESITO: [SUPERATO] Il protocollo impedisce la modifica diretta di referti attivi")
        superati += 1
    else:
        print("-> ESITO: [FALLITO] Aggiornamento illecito consentito")

    #reset dello stato originale
    clinica._database[paziente._ID][id_ref][0] = False


    # RIEPILOGO FINALE
    print("\n" + "=" * 65)
    print(f"RIEPILOGO TEST DI SICUREZZA: {superati}/{totali} SCENARI SUPERATI CON SUCCESSO")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    run_security_tests()
