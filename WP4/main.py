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
    # Il paziente richiede il referto (gestito tramite _receiveDocuments)
    paziente.ref_request(id_paziente, id_referto_univoco)

    print("\n=== TEST 3: RICHIESTA E SALVATAGGIO CHIAVI (KEY_REQ) ===")
    # Invia la richiesta per la chiave: RM risponde con KEY_SEND
    # attivando _receiveKey del paziente per memorizzarle in self._keys
    paziente.key_request(id_referto_univoco)

    print("\n=== TEST 4: REVOCA REFERTO (REVOKE) ===")
    motivo_revoca = "Errata trascrizione dell'esame del sangue."
    clinica.revokeReferto(id_paziente, id_referto_univoco, motivo_revoca)

    print("\n=== TEST 5: AGGIORNAMENTO REFERTO (UPDATE) ===")
    referto_aggiornato = "Referto Rettificato: Parametri corretti e confermati."
    clinica.updateReferto(id_paziente, id_referto_univoco, referto_aggiornato)

    print("\n=== TEST 6: VERIFICA DOPO AGGIORNAMENTO (REF_REQ) ===")
    paziente.ref_request(id_paziente, id_referto_univoco)