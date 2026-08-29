from CentralSystem.data.database import Database
from CentralSystem.rm import RM
from thirdParties.ca import CA
from globalClasses.enumerations import Role, OperationCode as oc
from users import Clinica
"""
r = Register()
r.addAudit(Audit(1,2,3,4))
r.addAudit(Audit(2,3,4,5))
d = r.serialize()
print(d)
l = r.deserialize(d)
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