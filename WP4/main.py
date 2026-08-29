from CentralSystem.data.register import Register
from CentralSystem.data.audit import Audit
r = Register()
r.addAudit(Audit(1,2,3,4))
r.addAudit(Audit(2,3,4,5))
d = r.serialize()
print(d)
l = r.deserialize(d)