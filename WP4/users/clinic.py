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

        #dato nel database gestito come [ Flag, CdR, MdR, referto ]
        self._database[IDpaziente][IDreferto] = [False, None, None, referto]
        return IDreferto

    def sendReferto(self, IDpaziente, IDreferto):

        #Controllo nome del referto: se il nome non inizia con l'ID della clinica
        #(ID considerato locale) lo trasforma in ID globale
        if not IDreferto.startswith(self._ID + "_"):
            IDreferto = self._ID + "_" + IDreferto

        if IDpaziente not in self._database or IDreferto not in self._database[IDpaziente]:
            print("Referto non esistente")
            return

        referto = self._database[IDpaziente][IDreferto][3]

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
        CdR = self._obtainCdR()
        self._database[IDpaziente][IDreferto][1] = CdR

        # concatenazione
        base = [IDreferto, CdR, False]
        sbase = Serializer.serialize(base)
        trev = S.Sign(self._kpriv, sbase)

        DdR = [ksimclinica, ksimpaziente, trev, CdR, creferto]

        message = [self._ID, oc.STORE, IDpaziente, IDreferto, DdR]

        IDrm = self._ca.getRMID()

        self.send(IDrm, message)


    #Revoca referto
    def revokeReferto(self, IDpaziente, IDreferto, MdR):
        if IDpaziente not in self._database:
            print("Referto non esistente")
            return
        if IDreferto not in self._database[IDpaziente]:
            print("Referto non esistente")
            return

        list = self._database[IDpaziente][IDreferto]
        list[0] = True
        list[2] = MdR

        krev = PiSim.GenSim()
        sign = S.Sign(self._kpriv, Serializer.serialize(MdR))

        MdRsign = [sign, MdR]
        crevoca = PiSim.EncSim(krev, Serializer.serialize(MdRsign))

        kpubpaziente = self._ca.getPublic(IDpaziente)

        krevpaziente, krevclinica = self._doublecrit(krev, kpubpaziente, self._kpub)

        #Ottenimento nuovo codice revoca
        CdR = self._obtainCdR()
        list[1] = CdR

        base = [IDreferto, CdR, True]

        trev = S.Sign(self._kpriv, Serializer.serialize(base))

        DdRev = [krevclinica, krevpaziente, trev, CdR, crevoca]

        message = [self._ID, oc.REVOKE, IDpaziente, IDreferto, DdRev]

        IDrm = self._ca.getRMID()

        self.send(IDrm, message)

    def updateReferto(self, IDpaziente, IDreferto, referto):
        if IDpaziente not in self._database:
            print("Referto non esistente")
            return
        if IDreferto not in self._database[IDpaziente]:
            print("Referto non esistente")
            return

        list = self._database[IDpaziente][IDreferto]
        list[0] = False
        list[3] = referto

        ksim = PiSim.GenSim()
        sign = S.Sign(self._kpriv, Serializer.serialize(referto))

        refsign = [sign, referto]
        creferto = PiSim.EncSim(ksim, Serializer.serialize(refsign))

        kpubpaziente = self._ca.getPublic(IDpaziente)

        ksimpaziente, ksimclinica = self._doublecrit(ksim, kpubpaziente, self._kpub)

        CdR = self._database[IDpaziente][IDreferto][1]

        base = [IDreferto, CdR, False]

        trev = S.Sign(self._kpriv, Serializer.serialize(base))

        DdRef = [ksimclinica, ksimpaziente, trev, creferto]

        message = [self._ID, oc.UPDATE, IDpaziente, IDreferto, DdRef]

        IDrm = self._ca.getRMID()

        self.send(IDrm, message)


    def ref_request(self, IDpaziente, IDreferto):
        self._ref_request(IDpaziente, IDreferto, None)

    def aud_request(self, IDpaziente, IDreferto):
        self._aud_request(IDpaziente, IDreferto, None)

    def send(self, dest, m):
        print(self._ID + ": Invio Messaggio")
        super().send(dest, m)

    def receive(self, c):
        print(self._ID + ": Messaggio ottenuto")
        super().receive(c)

    def _obtainCdR(self):
        a, b, c = random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)
        return str(a) + str(b) + str(c)