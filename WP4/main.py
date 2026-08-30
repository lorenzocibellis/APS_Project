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
    # 1. Inizializzazione della Certificate Authority e del Database
    ca = CA()
    db = Database()

    # 2. Creazione del Resource Manager (RM)
    # Registrazione automatica presso la CA e collegamento al ComunicationChannel
    rm = RM(Role.RM, ca, db)

    # 3. Creazione e iscrizione del Paziente e della Clinica
    paziente = Paziente(ca, rm)
    clinica = Clinica(ca, rm)

    id_paziente = paziente._ID
    id_referto = "REF_2026_001"
    contenuto_referto = "Referto medico 2026: Tutti i parametri sono nella norma."

    print("=== TEST 1: MEMORIZZAZIONE REFERTO ===")
    # La clinica cifra il referto ed invia l'operazione oc.STORE al RM
    clinica.createRefertoCifrato(id_paziente, id_referto, contenuto_referto)

    print("\n=== TEST 2: RICHIESTA REFERTO ===")
    # La clinica prepara e invia il messaggio di richiesta oc.REF_REQ al RM
    messaggio_richiesta = [clinica._ID, oc.REF_REQ, id_paziente, id_referto, None]
    id_rm = ca.getRMID()

    clinica.send(id_rm, messaggio_richiesta)