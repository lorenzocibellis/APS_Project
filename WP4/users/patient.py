from globalClasses.enumerations import Role
from users.userInterface import User
from globalClasses.enumerations import OperationCode as oc, NotifyCode as nc

class Paziente(User):


    def __init__(self, ca, rm):
        super().__init__(Role.PAZIENTE, ca, rm)
        self._keys = dict()

    def _receiveKey(self, message):
        if len(message) != 6:
            self._notify(nc.INVALID_DATA)
            return

        sender, _, IDpaziente, IDreferto, krev, ksim = message

        if sender != self._ca.getRMID():
            self._notify(nc.INVALID_OP)
            return

        if IDpaziente != self._ID:
            self._notify(nc.INVALID_DATA)
            return

        self._keys[IDreferto] = [krev, ksim]
        self._notify(nc.SUCCESS)

    def aud_request(self, IDreferto):
        self._aud_request(self._ID, IDreferto, None)

    def ref_request(self, IDreferto):
        self._ref_request(self._ID, IDreferto, None)

    def key_request(self,IDreferto):
        message = [self._ID, oc.KEY_REQ, IDreferto]
        IDrm = self._ca.getRMID()
        self.send(IDrm, message)