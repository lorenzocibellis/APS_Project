from cryptoOperation.cryptOp import S, PiAsim
from cryptoOperation.serializer import Serializer
from globalClasses.enumerations import Role
from users.userInterface import User
from globalClasses.enumerations import OperationCode as oc, NotifyCode as nc

class Medico(User):

    def __init__(self, ca, rm):
        super().__init__(Role.MEDICO, ca, rm)
        self._ksim = dict()
        self._krev = dict()
        self._auth = dict()

    def _storeAuth(self, Auth, IDpaziente, IDreferto):
        if IDpaziente not in self._auth:
            self._auth[IDpaziente] = dict()
        self._auth[IDpaziente][IDreferto] = Auth

    def _storeKeys(self, krev, ksim, IDpaziente):
        self._krev[IDpaziente] = krev
        self._ksim[IDpaziente] = ksim


    def _obtainKey(self, IDpaziente, IDclinica, DdRevoca, DdReferto):
        ksim, krev = super()._obtainKey(IDpaziente, IDclinica, DdRevoca, DdReferto)
        if ksim is None:
            ksimm = self._ksim[IDpaziente]
            if ksimm is not None:
                ksim = PiAsim.DecAsim(self._kpriv, ksimm)
        if krev is None:
            krevm = self._krev[IDpaziente]
            if krevm is not None:
                krev = PiAsim.DecAsim(self._kpriv, krevm)
        return ksim, krev


    def aud_request(self, IDpaziente, IDreferto):
        if IDpaziente not in self._auth:
            print("Autorizzazione non ottenuta da parte del Paziente " + IDpaziente)
            return
        if IDreferto not in self._auth[IDpaziente]:
            print("Autorizzazioen non ottenuta per il referto " + IDreferto)
            return
        auth = self._auth[IDpaziente][IDreferto]

        self._aud_request(IDpaziente, IDreferto, auth)

    def ref_request(self, IDpaziente, IDreferto):
        if IDpaziente not in self._auth:
            print("Autorizzazione non ottenuta da parte del Paziente " + IDpaziente)
            return
        if IDreferto not in self._auth[IDpaziente]:
            print("Autorizzazioen non ottenuta per il referto " + IDreferto)
            return
        auth = self._auth[IDpaziente][IDreferto]

        self._ref_request(IDpaziente, IDreferto, auth)

    def vis_request(self, IDpaziente, IDreferto):
        message = [self._ID, oc.VIS_REQ, IDpaziente, IDreferto]
        self.send(IDpaziente, message)

    def _receiveConfirm(self, m):
        if len(m) != 6:
            self._notify(nc.INVALID_DATA)
            return

        #spacchettamento messaggio
        IDmittente, _, IDmedico, IDreferto, confirm, token = m

        if self._ca.getRole(IDmittente) != Role.PAZIENTE:
            self._notify(nc.INVALID_DATA)
            return

        if IDmedico != self._ID:
            self._notify(nc.UNAUTH)
            return
        elif not confirm:
            self._notify(nc.UNAUTH)
            return
        elif token == None or len(token) != 3:
            self._notify(nc.INVALID_DATA)
            return

        krevm, ksimm, auth = token

        if auth == None or len(auth) != 5:
            self._notify(nc.INVALID_DATA)
            return

        sign, IDmedicoAuth, IDpazienteAuth, IDrefertoAuth, timeStamp = auth

        if IDmedicoAuth != self._ID or IDpazienteAuth != IDmittente or IDrefertoAuth != IDreferto:
            self._notify(nc.INVALID_DATA)
            return

        #verifica auth
        base = [IDmedicoAuth, IDpazienteAuth, IDrefertoAuth, timeStamp]
        kpub = self._ca.getPublic(IDmittente)
        if not S.Vrfy(kpub, Serializer.serialize(base), sign):
            self._notify(nc.INVALID_DATA)
            return
        #memorizzazione autorizzazione
        self._storeAuth(auth, IDmittente, IDreferto)


        #ottenimento e memorizzazione chiavi
        self._storeKeys(krevm, ksimm, IDmittente)