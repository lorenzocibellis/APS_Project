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