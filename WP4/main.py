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
from globalClasses.enumerations import Role, OperationCode as oc

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
    id_rm = ca.getRMID()

    print("=== TEST 1: CARICAMENTO REFERTO (STORE) ===")
    referto_iniziale = "Referto Iniziale: Valori ematici nella norma."
    clinica.createAndSendReferto(id_paziente, id_referto_locale, referto_iniziale)

    print("\n=== TEST 2: RICHIESTA REFERTO INIZIALE (REF_REQ) ===")
    richiesta_referto = [clinica._ID, oc.REF_REQ, id_paziente, id_referto_univoco, None]
    clinica.send(id_rm, richiesta_referto)

    print("\n=== TEST 3: REVOCA REFERTO (REVOKE) ===")
    motivo_revoca = "Errata trascrizione dell'esame del sangue."
    clinica.revokeReferto(id_paziente, id_referto_univoco, motivo_revoca)

    print("\n=== TEST 4: AGGIORNAMENTO REFERTO (UPDATE) ===")
    referto_aggiornato = "Referto Rettificato: Parametri corretti e confermati."
    # Invia l'aggiornamento al RM
    clinica.updateReferto(id_paziente, id_referto_univoco, referto_aggiornato)

    print("\n=== TEST 5: VERIFICA DOPO AGGIORNAMENTO (REF_REQ) ===")
    # Richiesta del referto aggiornato per verificare il reset della flag di revoca a False
    clinica.send(id_rm, richiesta_referto)