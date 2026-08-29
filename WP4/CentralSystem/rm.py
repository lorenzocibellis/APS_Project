from interfaces import Comunication
from CentralSystem.data.database import Database
from globalClasses.enumerations import OperationCode as oc, NotifyCode as nc
class RM(Comunication):


    def __init__(self, role, ca, db: Database):
        super().__init__(role, ca)
        self._db = db


    def receive(self, c):
        data = super().receive(c)
        if data is None:
            return
        m, sender, op, kpub, cnt, signaudit = data
        print("Elaborazione della richiesta")
        if op == oc.STORE:
            self._store(m, cnt, signaudit)
        elif op == oc.REF_REQ:
            self._getRef(m, cnt, signaudit)
        elif op == oc.KEY_REQ:
            self._getKey(m, cnt, signaudit)
        elif op == oc.REVOKE:
            self._revoke(m, cnt, signaudit)
        elif op == oc.UPDATE:
            self._revoke(m, cnt, signaudit)
        elif op == oc.AUD_REQ:
            self._getAuditing(m, cnt, signaudit)
        else:
            response = self._notifyMessage(sender ,nc.INVALID)

        print("RM : Richiesta elaborata")

        print("RM : Invio messaggio di risposta")


    def _store(self, m, cnt ,signaudit):
        if len(m) != 5:
           raise ValueError("Lunghezza del pacchetto errata")
        print(m)
        IDclinica, _ , IDpaziente , IDreferto, DdR = m
        ksimc, ksimp , trev, creferto = DdR
        error = self._db.addItem(IDpaziente, IDreferto, IDclinica, ksimp, ksimc, None, None, trev, None, creferto)
        if error == nc.SUCCESS:
            self._db.addAudit(IDpaziente, IDreferto, IDclinica, oc.STORE, cnt, signaudit)
        self._notifyMessage(IDclinica ,error)


    def _notifyMessage(self, receiver, code):
        message = [self._ID, oc.NOTIFY, code]
        self.send(receiver, message)
