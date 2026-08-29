import random
from enum import StrEnum

from cryptoOperation.serializer import Serializer
from interfaces import User
from cryptoOperation.cryptOp import PiSim, PiAsim, S

class Role(StrEnum):
    CLINICA = "Clinica"
    PAZIENTE = "Paziente"
    MEDICO = "Medico"
    RM = "Request Manager"



class Clinica(User):

    def __init__(self,ca, rm):
        super().__init__(Role.CLINICA,ca)
        self._rm = rm

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
        base = [IDreferto , Cdr, False]
        sbase = Serializer.serialize(base)
        trev = S.Sign(self._kpriv, base)

        DdR = [ksimclinica, ksimpaziente, trev, creferto]

        message = [self._ID, "00", IDpaziente, IDreferto, DdR]

        IDrm

        self.send(IDrm, message)



#class Paziente(Comunication):


#class Medico(Comunication):