import random

from cryptoOperation.serializer import Serializer
from interfaces import User
from cryptoOperation.cryptOp import PiSim, PiAsim, S
from globalClasses.enumerations import OperationCode as oc, Role


class Clinica(User):

    def __init__(self,ca, rm):
        super().__init__(Role.CLINICA,ca, rm)


    def createRefertoCifrato(self,IDpaziente, IDreferto ,referto):
        #generazione chiave simmetrica
        ksim = PiSim.GenSim()

        sign = S.Sign(self._kpriv, referto)
        refertosign = Serializer.serialize( [sign , referto] )
        creferto = PiSim.EncSim(ksim, refertosign)

        #si ottiene la chiave del paziente tramite CA
        kpubpaziente = self._ca.getPublic(IDpaziente)

        #si cifra la chiave simmetrica
        ksimpaziente, ksimclinica  = self._doublecrit(ksim, kpubpaziente, self._kpub)

        #creazione Codice della Revoca casuale
        a,b,c = random.randint(0,9), random.randint(0,9), random.randint(0,9)
        CdR = str(a) + str(b) + str(c)

        #concatenazione
        base = [IDreferto , CdR, False]
        sbase = Serializer.serialize(base)
        trev = S.Sign(self._kpriv, sbase)

        DdR = [ksimclinica, ksimpaziente, trev, CdR, creferto]

        message = [self._ID, oc.STORE, IDpaziente, IDreferto, DdR]

        IDrm = self._ca.getRMID()
        self.send(IDrm, message)

    def send(self, dest, m):
        print(self._ID + ": Invio Messaggio")
        super().send(dest, m)

    def receive(self, c):
        print(self._ID + ": Messaggio ottenuto")
        super().receive(c)
        

class Paziente(User):
    def __init__(self, ca, rm):
        super().__init__(Role.PAZIENTE, ca, rm)



class Medico(User):

    def __init__(self, ca, rm):
        super().__init__(Role.MEDICO, ca, rm)
        self._ksim = dict()
        self._krev = dict()

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
