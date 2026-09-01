from datetime import timezone, datetime

from cryptoOperation.cryptOp import PiAsim, S
from cryptoOperation.serializer import Serializer
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

    def _receiveRequest(self, m):
        if len(m) != 4:
            self._notify(nc.INVALID_DATA)
            return

        IDmedico, _, IDpaziente, IDreferto = m

        if self._ca.getRole is None or self._ca.getRole(IDmedico) != Role.MEDICO:
            self._notifyMessage(IDmedico, nc.UNAUTH)
            return

        if self._ID != IDpaziente:
            self._notify(nc.INVALID_DATA)
            return

        confirm = input("Dare autorizzazione al medico?\n Inviare 1 se si, qualsiasi altra cosa altrimenti\n")

        if confirm == "1":
            self.key_request(IDreferto)

            if IDreferto not in self._keys:
                self._notifyMessage(IDmedico, nc.INVALID_DATA)
                return

            krevp, ksimp = self._keys[IDreferto]
            kpub = self._ca.getPublic(IDmedico)

            ksimm, krevm = None, None
            if ksimp is not None:
                ksim = PiAsim.DecAsim(self._kpriv, ksimp)
                ksimm = PiAsim.EncAsim(kpub, ksim)
            if krevp is not None:
                krev = PiAsim.DecAsim(self._kpriv, krevp)
                krevm = PiAsim.EncAsim(kpub, krev)


            time = datetime.now(timezone.utc)
            auth = [IDmedico, self._ID, IDreferto, time]
            sign = S.Sign(self._kpriv, Serializer.serialize(auth))

            auth.insert(0, sign)

            Token = [krevm, ksimm, auth]
            flag = True
        else:
            Token = None
            flag = False

        message = [self._ID, oc.CONFIRM, IDmedico, IDreferto, flag, Token]
        self.send(IDmedico, message)



    def _notifyMessage(self, receiver, code):
        message = [self._ID, oc.NOTIFY, code]
        print(self._ID + " : Invio messaggio di risposta")
        self.send(receiver, message)


