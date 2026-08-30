import random

from cryptoOperation.serializer import Serializer
from comunicationInterface import Comunication
from cryptoOperation.cryptOp import PiSim, PiAsim, S
from globalClasses.enumerations import OperationCode as oc, NotifyCode as nc



class User(Comunication):

    def __init__(self,role, ca, rm):
        super().__init__(role, ca)
        self._rm = rm

    #metodo che permette la cifratura di una chiave usando 2 chiavi diverse tramite cifrtura asimmetrica
    def _doublecrit(self,k, k1, k2):
        k1c = PiAsim.EncAsim(k,k1)
        k2c = PiAsim.EncAsim(k,k2)
        return k1c,k2c

    def receive(self, c):
        data = super().receive(c)
        if data is None:
            return
        if len(data) != 3:
            self._notify(nc.INVALID_DATA)
            return

        m , op, kpub = data

        if op == oc.NOTIFY:
            self._notify(m[1])
        if op == oc.REF_SEND:
            self._obtainDocuments(m)

    def _notify(self,code):
        if code == nc.SUCCESS:
            print(self._ID + ": Operazione svolta con successo!!")
        elif code == nc.INVALID_DATA:
            print(self._ID + ": Operazione non effettuata: Dati non validi")
        elif code == nc.UNAUTH:
            print(self._ID + ": Operazione non effettuata: Autorizzazione negata")
        elif code == nc.INEX:
            print(self._ID + ": Operazione non effettuata: identificativo inesistente")


    def _obtainDocuments(self, message):
        if len(message) != 8:
            self._notify(nc.INVALID_DATA)
            return

        #Ottenenedo dati di Pre-Condizione
        IDsender, _, IDclinica, IDpaziente, IDreferto, FdR, DdRevoca, DdReferto = message
        kpub = self._ca.getPublic(IDclinica)

        #ottenimento chiavi simmetriche
        ksim, krev = self._obtainKey(IDpaziente, IDclinica, DdRevoca, DdReferto)

        if len(DdRevoca) != 4 or len(DdReferto) != 2:
            self._notify(nc.INVALID_DATA)
            return

        #Ottenimento documenti cifrati
        _, trev, CdR, crevoca = DdRevoca
        _, creferto = DdReferto

        #Fine ottenimento dati di Pre-Condizione

        #Estrazione documento
        mreferto = PiSim.DecSim(ksim, creferto)
        mreferto = Serializer.deserialize(mreferto)
        signreferto, referto = mreferto

        mrevoca = PiSim.DecSim(krev, crevoca)
        mrevoca = Serializer.deserialize(mrevoca)
        signrevoca, MdR = mrevoca

        #validazione metadati di revoca
        base = [IDreferto, CdR, FdR]
        sbase = Serializer.serialize(base)
        if not S.Vrfy(kpub, sbase, trev):
            self._notify(nc.INVALID_DATA)
            return

        #verifica dei documenti
        if not S.Vrfy(kpub, Serializer.serialize(referto), signreferto) or not S.Vrfy(kpub, Serializer.serialize(MdR), signrevoca):
            self._notify(nc.INVALID_DATA)
            return

        print("Documenti ottenuti validi!")
        self._printDocuments(referto, FdR, MdR)
        return


    def _printDocuments(self, ref, f, rev):
        if f:
            print("ATTENZIONE: DOCUMENTO REVOCATO\nMOTIVAZINE: " + rev)
        print(ref)


    def _obtainKey(self, IDpaziente, IDclinica, DdRevoca, DdReferto):
        paziente = IDpaziente
        clinica = IDclinica
        return DdReferto[0], DdRevoca[0]





