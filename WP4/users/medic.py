from globalClasses.enumerations import Role
from users.userInterface import User


class Medico(User):

    def __init__(self, ca, rm):
        super().__init__(Role.MEDICO, ca, rm)
        self._ksim = dict()
        self._krev = dict()
        self._auth = dict()

    def _storeAuth(self, Auth, IDpaziente):
        self._auth[IDpaziente] = Auth

    def _storeKeys(self, krev, ksim, IDpaziente):
        self._krev[IDpaziente] = krev
        self._ksim[IDpaziente] = ksim


    def _obtainKey(self, IDpaziente, IDclinica, DdRevoca, DdReferto):
        ksim, krev = super()._obtainKey(IDpaziente, IDclinica, DdRevoca, DdReferto)
        if ksim is None:
            ksim = self._ksim[IDpaziente]
        if krev is None:
            krev = self._krev[IDpaziente]

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