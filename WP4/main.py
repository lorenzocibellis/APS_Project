from CentralSystem.data.register import Register
from CentralSystem.data.audit import Audit
from CentralSystem.rm import RM
from cryptoOperation.serializer import Serializer
from interfaces import Comunication
from thirdParties.ca import CA
from thirdParties.comunicationChannel import ComunicationChannel
from users import Role

r = Register()
r.addAudit(Audit(1,2,3,4))
r.addAudit(Audit(2,3,4,5))
d = r.serialize()
print(d)
l = r.deserialize(d)


ca = CA()
rm = RM(Role.RM , ca)
m = ("RM0", "00" , 21, 12, [0,0,0,0])
rm.send(rm._ID, m , [m[0], m[1]])
