import random

from cryptoOperation.cryptOp import PiSim, S
from cryptoOperation.serializer import Serializer
from globalClasses.enumerations import Role
from users.userInterface import User
from globalClasses.enumerations import OperationCode as oc

class Clinica(User):


    def __init__(self, ca, rm):
        super().__init__(Role.CLINICA, ca, rm)
        self._database = dict()

    def createAndSendReferto(self, IDpaziente, IDreferto, referto):
        IDreferto = self.createReferto(IDpaziente, IDreferto, referto)
        if IDreferto is None:
            return
        self.sendReferto(IDpaziente,IDreferto)


    def createReferto(self, IDpaziente, IDreferto, referto):
        # creazione nuovo ID del referto
        IDreferto = self._ID + "_" + IDreferto
        # Controllo unicità del referto
        if IDpaziente not in self._database:
            self._database[IDpaziente] = dict()
        else:
            if IDreferto in self._database[IDpaziente]:
                print("Referto già presente")
                return
        self._database[IDpaziente][IDreferto] = [False, None, referto]
        return IDreferto

    def sendReferto(self, IDpaziente, IDreferto):

        #Controllo nome del referto: se il nome non inizia con l'ID della clinica
        #(ID considerato locale) lo trasforma in ID globale
        if not IDreferto.startswith(self._ID + "_"):
            IDreferto = self._ID + "_" + IDreferto

        if IDpaziente not in self._database or IDreferto not in self._database[IDpaziente]:
            print("Referto non esistente")
            return

        referto = self._database[IDpaziente][IDreferto]

        # generazione chiave simmetrica
        ksim = PiSim.GenSim()

        sign = S.Sign(self._kpriv, Serializer.serialize(referto))
        refertosign = Serializer.serialize([sign, referto])
        creferto = PiSim.EncSim(ksim, refertosign)

        # si ottiene la chiave del paziente tramite CA
        kpubpaziente = self._ca.getPublic(IDpaziente)

        # si cifra la chiave simmetrica
        ksimpaziente, ksimclinica = self._doublecrit(ksim, kpubpaziente, self._kpub)

        # creazione Codice della Revoca casuale
        a, b, c = random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)
        CdR = str(a) + str(b) + str(c)

        # concatenazione
        base = [IDreferto, CdR, False]
        sbase = Serializer.serialize(base)
        trev = S.Sign(self._kpriv, sbase)

        DdR = [ksimclinica, ksimpaziente, trev, CdR, creferto]

        message = [self._ID, oc.STORE, IDpaziente, IDreferto, DdR]

        IDrm = self._ca.getRMID()

        self.send(IDrm, message)

    def revokeReferto(self, IDreferto):
        pass

    def send(self, dest, m):
        print(self._ID + ": Invio Messaggio")
        super().send(dest, m)

    def receive(self, c):
        print(self._ID + ": Messaggio ottenuto")
        super().receive(c)
