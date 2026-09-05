from CentralSystem.data.database import Database
from CentralSystem.rm import RM
from thirdParties.ca import CA
from globalClasses.enumerations import Role, OperationCode as oc
from users.clinic import Clinica
"""
r = Register()
r.addAudit(Audit(1,2,3,4))
r.addAudit(Audit(2,3,4,5))
d = r.serialize()
print(d)
l = r.deserialize(d)
"""

"""
db = Database()
ca = CA()
rm = RM(Role.RM , ca, db)
c1 = Clinica(ca,rm)
cr = "cifrato bro"
DdR = ["k1", "k2", "trev", cr]
m = (c1._ID, oc.STORE , 21, 12, DdR)
c1.send(rm._ID, m)


while 1:
    flag = input("Inviare messaggio?")
    if flag:
        rm.send(rm._ID, m )
        print("Messaggio non inviato")
    else:
        print("Messaggio non inviato")
        
        """

"""
from CentralSystem.data.database import Database
from CentralSystem.rm import RM
from thirdParties.ca import CA
from users.clinic import Clinica
from users.patient import Paziente
from globalClasses.enumerations import Role

if __name__ == "__main__":
    # 1. Inizializzazione CA, Database e Resource Manager (RM)
    ca = CA()
    db = Database()
    rm = RM(Role.RM, ca, db)

    # 2. Inizializzazione degli attori
    paziente = Paziente(ca, rm)
    clinica = Clinica(ca, rm)

    id_paziente = paziente._ID
    id_referto_locale = "REF_2026_001"
    id_referto_univoco = f"{clinica._ID}_{id_referto_locale}"

    print("=== TEST 1: CARICAMENTO REFERTO (STORE) ===")
    referto_iniziale = "Referto Iniziale: Valori ematici nella norma."
    clinica.createAndSendReferto(id_paziente, id_referto_locale, referto_iniziale)

    print("\n=== TEST 2: RICHIESTA REFERTO DAL PAZIENTE (REF_REQ) ===")
    paziente.ref_request(id_referto_univoco)

    print("\n=== TEST 3: RICHIESTA CHIAVI DAL PAZIENTE (KEY_REQ) ===")
    paziente.key_request(id_referto_univoco)

    print("\n=== TEST 4: REVOCA REFERTO (REVOKE) ===")
    motivo_revoca = "Errata trascrizione dell'esame del sangue."
    clinica.revokeReferto(id_paziente, id_referto_univoco, motivo_revoca)

    print("\n=== TEST 5: AGGIORNAMENTO REFERTO (UPDATE) ===")
    referto_aggiornato = "Referto Rettificato: Parametri corretti e confermati."
    clinica.updateReferto(id_paziente, id_referto_univoco, referto_aggiornato)

    print("\n=== TEST 6: RICHIESTA REGISTRO DI AUDIT (AUD_REQ) ===")
    # Il paziente richiede al RM il registro di tracciamento per il referto specificato
    paziente.aud_request(id_referto_univoco)

    print("\n=== TEST 7: VERIFICA REGISTRO DI AUDIT OTTENUTO ===")
    # Stampa del registro salvato in self._registers dell'utente previa verifica crittografica degli audit
    if id_referto_univoco in paziente._registers:
        registro = paziente._registers[id_referto_univoco]
        print(registro)
    else:
        print("Registro di audit non presente o non valido.")
"""
"""
from CentralSystem.data.database import Database
from CentralSystem.rm import RM
from thirdParties.ca import CA
from users.clinic import Clinica
from users.patient import Paziente
from users.medic import Medico
from globalClasses.enumerations import Role

if __name__ == "__main__":
    # 1. Inizializzazione CA, Database e Resource Manager (RM)
    ca = CA()
    db = Database()
    rm = RM(Role.RM, ca, db)

    # 2. Inizializzazione degli attori
    paziente = Paziente(ca, rm)
    clinica = Clinica(ca, rm)
    medico = Medico(ca, rm)

    id_paziente = paziente._ID
    id_referto_locale = "REF_2026_001"
    id_referto_univoco = f"{clinica._ID}_{id_referto_locale}"

    print("=== TEST 1: CARICAMENTO REFERTO (STORE) ===")
    referto_iniziale = "Referto Iniziale: Valori ematici nella norma."
    clinica.createAndSendReferto(id_paziente, id_referto_locale, referto_iniziale)

    print("\n=== TEST 2: RICHIESTA AUTORIZZAZIONE DAL MEDICO (VIS_REQ & CONFIRM) ===")
    # Il medico richiede l'autorizzazione al paziente (interattivo: inserire 1 a terminale)
    medico.vis_request(id_paziente, id_referto_univoco)

    print("\n=== TEST 3: RICHIESTA REFERTO DAL MEDICO (REF_REQ) ===")
    # Il medico richiede il referto cifrato al RM usando il token di autorizzazione ottenuto
    medico.ref_request(id_paziente, id_referto_univoco)

    print("\n=== TEST 4: RICHIESTA REGISTRO DI AUDIT DAL MEDICO (AUD_REQ) ===")
    # Il medico richiede il registro di tracciamento al RM per il referto del paziente
    medico.aud_request(id_paziente, id_referto_univoco)

    print("\n=== TEST 5: VERIFICA REGISTRO DI AUDIT OTTENUTO DAL MEDICO ===")
    # Verifica del registro salvato nel sotto-dizionario del medico [id_paziente][id_referto]
    if id_paziente in medico._registers and id_referto_univoco in medico._registers[id_paziente]:
        registro = medico._registers[id_paziente][id_referto_univoco]
        print("Registro di audit valido ottenuto dal Medico:")
        print(registro)
    else:
        print("Registro di audit non presente o non valido per il Medico.")

"""

from CentralSystem.data.database import Database
from CentralSystem.rm import RM
from thirdParties.ca import CA
from users.clinic import Clinica
from users.patient import Paziente
from users.medic import Medico
from globalClasses.enumerations import Role


def menu_clinica(clinica):
    while True:
        print(f"\n--- MENU CLINICA (ID: {clinica._ID}) ---")
        print("1. Crea e Invia Referto")
        print("2. Revoca Referto")
        print("3. Aggiorna Referto")
        print("4. Richiedi Referto (ref_request)")
        print("5. Richiedi Registro di Audit (aud_request)")
        print("6. Visualizza Registri di Audit Salvati")
        print("0. Torna al menu principale")

        scelta = input("Seleziona un'operazione: ").strip()

        if scelta == "1":
            id_paziente = input("ID Paziente: ").strip()
            id_referto_locale = input("ID Referto Locale (es. REF_001): ").strip()
            contenuto = input("Contenuto del referto: ").strip()
            clinica.createAndSendReferto(id_paziente, id_referto_locale, contenuto)
        elif scelta == "2":
            id_paziente = input("ID Paziente: ").strip()
            id_referto = input("ID Referto Univoco (es. CLINICA_ID_REF_001): ").strip()
            motivo = input("Motivo della revoca: ").strip()
            clinica.revokeReferto(id_paziente, id_referto, motivo)
        elif scelta == "3":
            id_paziente = input("ID Paziente: ").strip()
            id_referto = input("ID Referto Univoco (es. CLINICA_ID_REF_001): ").strip()
            nuovo_contenuto = input("Nuovo contenuto referto: ").strip()
            clinica.updateReferto(id_paziente, id_referto, nuovo_contenuto)
        elif scelta == "4":
            id_paziente = input("ID Paziente: ").strip()
            id_referto = input("ID Referto Univoco (es. CLINICA_ID_REF_001): ").strip()
            clinica.ref_request(id_paziente, id_referto)
        elif scelta == "5":
            id_paziente = input("ID Paziente: ").strip()
            id_referto = input("ID Referto Univoco (es. CLINICA_ID_REF_001): ").strip()
            clinica.aud_request(id_paziente, id_referto)
        elif scelta == "6":
            print("\n[Registri di Audit salvati localmente dalla Clinica]")
            if clinica._registers:
                for paz_id, refs in clinica._registers.items():
                    for ref_id, reg in refs.items():
                        print(f"-> Paziente {paz_id}, Referto {ref_id}:\n{reg}")
            else:
                print("Nessun registro presente.")
        elif scelta == "0":
            break
        else:
            print("Opzione non valida.")


def menu_paziente(paziente):
    while True:
        print(f"\n--- MENU PAZIENTE (ID: {paziente._ID}) ---")
        print("1. Richiedi Chiavi Referto (key_request)")
        print("2. Richiedi Referto Cifrato (ref_request)")
        print("3. Richiedi Registro di Audit (aud_request)")
        print("4. Visualizza Registri di Audit Salvati")
        print("0. Torna al menu principale")

        scelta = input("Seleziona un'operazione: ").strip()

        if scelta == "1":
            id_referto = input("ID Referto Univoco (es. C0_REF_001): ").strip()
            paziente.key_request(id_referto)
        elif scelta == "2":
            id_referto = input("ID Referto Univoco (es. C0_REF_001): ").strip()
            paziente.ref_request(id_referto)
        elif scelta == "3":
            id_referto = input("ID Referto Univoco (es. C0_REF_001): ").strip()
            paziente.aud_request(id_referto)
        elif scelta == "4":
            print("\n[Registri di Audit salvati localmente]")
            if paziente._registers:
                for ref_id, reg in paziente._registers.items():
                    print(f"-> Referto {ref_id}:\n{reg}")
            else:
                print("Nessun registro presente.")
        elif scelta == "0":
            break
        else:
            print("Opzione non valida.")


def menu_medico(medico):
    while True:
        print(f"\n--- MENU MEDICO (ID: {medico._ID}) ---")
        print("1. Richiedi Autorizzazione al Paziente (vis_request)")
        print("2. Richiedi Referto Cifrato a RM (ref_request)")
        print("3. Richiedi Registro di Audit a RM (aud_request)")
        print("4. Visualizza Autorizzazioni e Registri Salvati")
        print("0. Torna al menu principale")

        scelta = input("Seleziona un'operazione: ").strip()

        if scelta == "1":
            id_paziente = input("ID Paziente: ").strip()
            id_referto = input("ID Referto Univoco (es. C0_REF_001): ").strip()
            medico.vis_request(id_paziente, id_referto)
        elif scelta == "2":
            id_paziente = input("ID Paziente: ").strip()
            id_referto = input("ID Referto Univoco (es. C0_REF_001): ").strip()
            medico.ref_request(id_paziente, id_referto)
        elif scelta == "3":
            id_paziente = input("ID Paziente: ").strip()
            id_referto = input("ID Referto Univoco (es. C0_REF_001): ").strip()
            medico.aud_request(id_paziente, id_referto)
        elif scelta == "4":
            print("\n[Autorizzazioni Salvate]")
            print(medico._auth)
            print("\n[Registri di Audit Salvati]")
            print(medico._registers)
        elif scelta == "0":
            break
        else:
            print("Opzione non valida.")


def registraNuovoUtente(ca, rm, cliniche, pazienti, medici):
    print("\n--- REGISTRAZIONE NUOVO UTENTE ---")
    print("1. Nuova Clinica")
    print("2. Nuovo Paziente")
    print("3. Nuovo Medico")
    print("0. Annulla")

    scelta = input("Seleziona tipo di utente: ").strip()

    if scelta == "1":
        nuovo = Clinica(ca, rm)
        cliniche.append(nuovo)
        print(f"\n[+] Creata con successo Clinica (ID: {nuovo._ID})")
    elif scelta == "2":
        nuovo = Paziente(ca, rm)
        pazienti.append(nuovo)
        print(f"\n[+] Creato con successo Paziente (ID: {nuovo._ID})")
    elif scelta == "3":
        nuovo = Medico(ca, rm)
        medici.append(nuovo)
        print(f"\n[+] Creato con successo Medico (ID: {nuovo._ID})")
    elif scelta == "0":
        return
    else:
        print("Scelta non valida.")


def main():
    ca = CA()
    db = Database()
    rm = RM(Role.RM, ca, db)

    # 2 utenti di default per ogni categoria
    cliniche = [Clinica(ca, rm), Clinica(ca, rm)]      # C0, C1
    pazienti = [Paziente(ca, rm), Paziente(ca, rm)]    # P0, P1
    medici = [Medico(ca, rm), Medico(ca, rm)]          # M0, M1

    while True:
        print("\n==========================================")
        print("   SISTEMA DI GESTIONE REFERTI MEDICI    ")
        print("==========================================")
        print("Seleziona l'utente con cui operare:")

        menu_map = {}
        idx = 1

        print("\n--- CLINICHE ---")
        for c in cliniche:
            print(f"{idx}. Clinica (ID: {c._ID})")
            menu_map[str(idx)] = ("Clinica", c)
            idx += 1

        print("\n--- PAZIENTI ---")
        for p in pazienti:
            print(f"{idx}. Paziente (ID: {p._ID})")
            menu_map[str(idx)] = ("Paziente", p)
            idx += 1

        print("\n--- MEDICI ---")
        for m in medici:
            print(f"{idx}. Medico (ID: {m._ID})")
            menu_map[str(idx)] = ("Medico", m)
            idx += 1

        print("\n--- GESTIONE UTENTI ---")
        idx_registra = str(idx)
        print(f"{idx_registra}. Registra nuovo utente")
        print("0. Esci")

        scelta = input("\nScelta: ").strip()

        if scelta == "0":
            print("\nChiusura dell'applicazione.")
            break
        elif scelta == idx_registra:
            registraNuovoUtente(ca, rm, cliniche, pazienti, medici)
        elif scelta in menu_map:
            ruolo, utente = menu_map[scelta]
            if ruolo == "Clinica":
                menu_clinica(utente)
            elif ruolo == "Paziente":
                menu_paziente(utente)
            elif ruolo == "Medico":
                menu_medico(utente)
        else:
            print("Scelta non valida.")


if __name__ == "__main__":
    main()