from cryptoOperation.cryptOp import PiAsim, PiSim, S
from cryptoOperation.serializer import Serializer
from globalClasses.enumerations import OperationCode as oc, NotifyCode as nc


class Comunication:

    _auditOp = [oc.STORE , oc.REF_REQ , oc.KEY_REQ , oc.REVOKE , oc.UPDATE, oc.AUD_REQ]

    def __init__(self, role, ca):
        self._role = role
        self._ID = None
        self._kpriv = None
        self._kpub = None
        self._identity = False
        self._cc = None
        self._ca = ca
        self._obtainIdentity()
        self._cntout = dict()
        self._cntin = dict()


    def _notifyMessage(self, receiver, code):
        pass

    def _existentID(self, ID):
        if self._ca.getRole(ID) is None:
            return False
        return True

    # inizializzazione identità presso una CA
    def _obtainIdentity(self):
        if not self._identity:
            self._kpriv, self._kpub = PiAsim.GenAsim(2048)
            self._ID = self._ca.subscribe(self, self._role, self._kpub)
            self._identity = True
            return
        print("Identità già inizializzata")


    def _getcntout(self, ID):
        return self._cntout[ID]

    def _getcntin(self, ID):
        return self._cntin[ID]

    def _cntupdateout(self, ID, new):
        self._cntout[ID] = new

    def _cntupdatein(self, ID, new):
        self._cntin[ID] = new

    def _cntinitializeout(self, ID):
        self._cntupdateout(ID, 0)

    def _cntinitializein(self, ID):
        self._cntupdatein(ID, 0)


    def send(self, dest, m):

        if dest not in self._cntout:
            self._cntinitializeout(dest)
        op = m[1]
        # passo 1
        ksim = PiSim.GenSim()

        # passo 2
        cnt = self._getcntout(dest)
        cnt = cnt + 1

        mcnt = [cnt , m]

        self._cntupdateout(dest, cnt)

        # passo 3
        kpub = self._ca.getPublic(dest)

        # passo 4
        smcnt = Serializer.serialize(mcnt)
        sign = S.Sign(self._kpriv, smcnt)



        # passo 5
        mcnt.insert(0,sign)
        msign = mcnt

        # operazione Audit
        if op in self._auditOp:
            audit = [m[0] , m[1] , cnt]
            audit = Serializer.serialize(audit)
            signaudit = S.Sign(self._kpriv, audit)
            msign.insert(0,signaudit)


        # passo 6
        msign = Serializer.serialize(msign)
        csign = PiSim.EncSim(ksim, msign)

        # passo 7
        kc = PiAsim.EncAsim(kpub, ksim)

        # passo 8
        c = [kc , csign]

        # passo 9
        self._cc.send(dest, c)
        return

    def receive(self, c):
        flag = False

        # passo 1
        kc, csign = c

        # passo 2
        ksim = PiAsim.DecAsim(self._kpriv, kc)

        #passo3
        msign = PiSim.DecSim(ksim, csign)
        msign = Serializer.deserialize(msign)

        #passo 4
        op = msign[-1][1]
        if op in self._auditOp:
            flag = True
            signaudit, sign , cnt , m = msign
        else:
            sign,cnt,m = msign
            signaudit = None

        IDsender = m[0]
        if IDsender not in self._cntin:
            self._cntin[IDsender] = 0

        # passo 5
        kpub = self._ca.getPublic(IDsender)

        # passo 5.5
        if signaudit is not None:
            audit = [m[0] , m[1] , cnt]
            saudit = Serializer.serialize(audit)
            if not S.Vrfy(kpub, saudit, signaudit):
                raise ValueError("Errore nella firma dell'audit")
            print(self._ID + ": Firma Audit verificata")

        # passo 6
        if not cnt > self._getcntin(IDsender):
            raise ValueError("Attacco Replay")

        # passo 7
        if not S.Vrfy(kpub, Serializer.serialize([cnt , m]), sign):
            self._notifyMessage(IDsender, nc.INVALID_DATA)
            return None

        self._cntupdatein(IDsender, cnt)
        print(self._ID + ": messaggio autenticato e validato")

        if flag:
            return [m , IDsender, op , kpub , cnt, signaudit]

        return [m , op, kpub]















