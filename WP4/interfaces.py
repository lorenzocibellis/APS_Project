from cryptoOperation.cryptOp import PiAsim, PiSim, S
from cryptoOperation.serializer import Serializer
from thirdParties.comunicationChannel import ComunicationChannel

class Referto:
    data = None

    def __init__(self,data):
        self.data = data


class Comunication:
    _role = None
    _ID = None
    _kpriv = None
    _kpub = None
    _identity = False
    _cntout = dict()
    _cntin = dict()
    _cc = None

    _auditOp = ["00" , "01" , "05" , "07" , "08"]

    def __init__(self, role, ca):
        self._role = role
        self._ca = ca
        self._obtainIdentity(ca)


    # inizializzazione identità presso una CA
    def _obtainIdentity(self, ca):
        if not self._identity:
            self._kpriv, self._kpub = PiAsim.GenAsim(2048)
            self._ID = ca.subscribe(self, self._role, self._kpub)
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


    def send(self, dest, m, audit = None):

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
            if audit is None:
                raise ValueError
            audit.append(cnt)
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
        self._cc.get(dest).receive(c)
        return

    def receive(self, c):
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
            signaudit, sign , cnt , m = msign
        else:
            sign,cnt,m = msign
            signaudit = None

        ID = m[0]
        if ID not in self._cntin:
            self._cntin[ID] = 0

        # passo 5
        kpub = self._ca.getPublic(ID)

        # passo 5.5
        if signaudit is not None:
            audit = [m[0] , m[1] , cnt]
            audit = Serializer.serialize(audit)
            if not S.Vrfy(kpub, audit, signaudit):
                raise ValueError("Errore nella firma dell'audit")
            print("Firma Audit verificata")

        # passo 6
        if not cnt > self._getcntin(ID):
            raise ValueError("Attacco Replay")

        # passo 7
        if not S.Vrfy(kpub, Serializer.serialize([cnt , m]), sign):
            raise ValueError("Messaggio non valido")

        self._cntupdatein(ID, cnt)
        print("messaggio autenticato")

        self._lastMessage = m
        return


