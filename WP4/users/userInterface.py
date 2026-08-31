import random
from io import UnsupportedOperation

from cryptoOperation.serializer import Serializer
from comunicationInterface import Comunication
from cryptoOperation.cryptOp import PiSim, PiAsim, S, H
from globalClasses.enumerations import OperationCode as oc, NotifyCode as nc, Role


class User(Comunication):


    def __init__(self,role, ca, rm):
        super().__init__(role, ca)
        self._rm = rm
        self._registers = dict()

    #metodo che permette la cifratura di una chiave k usando 2 chiavi diverse k1 e k2 tramite cifrtura asimmetrica
    def _doublecrit(self,k, k1, k2):
        k1c = PiAsim.EncAsim(k1, k)
        k2c = PiAsim.EncAsim(k2, k)
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
            self._notify(m[2])
        elif op == oc.REF_SEND:
            self._receiveDocuments(m)
        elif op == oc.KEY_SEND:
            self._receiveKey(m)
        elif op == oc.AUD_SEND:
            self._receiveAudit(m)
        else:
            self._notify(nc.INVALID_OP)

    def _notify(self,code):
        if code == nc.SUCCESS:
            print(self._ID + ": Operazione svolta con successo!!")
        elif code == nc.INVALID_DATA:
            print(self._ID + ": Operazione non effettuata: Dati non validi")
        elif code == nc.UNAUTH:
            print(self._ID + ": Operazione non effettuata: Autorizzazione negata")
        elif code == nc.INEX:
            print(self._ID + ": Operazione non effettuata: identificativo inesistente")
        elif code == nc.INVALID_OP:
            print(self._ID + ": Operazione non effettuata: operazione non valida")



    def _receiveAudit(self, message):
        if len(message) != 5:
            self._notify(nc.INVALID_DATA)
            return

        if message[0] != self._ca.getRMID():
            self._notify(nc.INVALID_DATA)
            return

        #Spacchettamento messaggio
        IDsender, _, IDpaziente, IDreferto, register = message

        if not self._verifyRegister(register):
            self._notify(nc.INVALID_DATA)
            return
        else:
            print("Registro di tracciamento ottenuto valido!")
            print(register)

        if self._role == Role.PAZIENTE:
            if self._ID != IDpaziente:
                self._notify(nc.INVALID_DATA)
                return
            else:
                self._registers[IDreferto] = register
        else:
            if IDpaziente not in self._registers:
                self._registers[IDpaziente] = dict()
            self._registers[IDpaziente][IDreferto] = register

    def _verifyRegister(self,r):
        for index in range(len(r)):
            audit, hash = r.getAudit(index)

            ID, op, cnt, sign = audit.getAll()
            kpub = self._ca.getPublic(ID)

            if not S.Vrfy(kpub, Serializer.serialize([ID, op, cnt]), sign):
                return False

            if index == 0:
                precHash = r.getGenesis()
            else:
                _, precHash = r.getAudit(index - 1)

            if not H.HVrfy(Serializer.serialize(audit) + b"|" + precHash, hash):
                return False
        return True

    def _receiveDocuments(self, message):
        if len(message) != 8:
            self._notify(nc.INVALID_DATA)
            return

        if message[0] != self._ca.getRMID():
            print("Mittente non valido")
            return
        #Ottenenedo dati di Pre-Condizione
        IDsender, _, IDclinica, IDpaziente, IDreferto, FdR, DdRevoca, DdReferto = message
        kpub = self._ca.getPublic(IDclinica)

        if len(DdRevoca) != 4 or len(DdReferto) != 2:
            self._notify(nc.INVALID_DATA)
            return

        #ottenimento chiavi simmetriche
        ksim, krev = self._obtainKey(IDpaziente, IDclinica, DdRevoca, DdReferto)



        #Ottenimento documenti cifrati
        _, trev, CdR, crevoca = DdRevoca
        _, creferto = DdReferto

        #Fine ottenimento dati di Pre-Condizione

        # validazione metadati di revoca
        base = [IDreferto, CdR, FdR]
        sbase = Serializer.serialize(base)
        if not S.Vrfy(kpub, sbase, trev):
            self._notify(nc.INVALID_DATA)
            return

        #Estrazione documento
        mreferto = PiSim.DecSim(ksim, creferto)
        mreferto = Serializer.deserialize(mreferto)
        signreferto, referto = mreferto
        if FdR:
            mrevoca = PiSim.DecSim(krev, crevoca)
            mrevoca = Serializer.deserialize(mrevoca)
            signrevoca, MdR = mrevoca
            #verifica revoca
            if not S.Vrfy(kpub, Serializer.serialize(MdR), signrevoca):
                self._notify(nc.INVALID_DATA)
                return
        else:
            MdR = None

        #verifica del referto
        if not S.Vrfy(kpub, Serializer.serialize(referto), signreferto):
            self._notify(nc.INVALID_DATA)
            return

        print("Documenti ottenuti validi!")
        self._printDocuments(referto, FdR, MdR)



    def _printDocuments(self, ref, f, rev):
        if f:
            print("ATTENZIONE: DOCUMENTO REVOCATO\nMOTIVAZINE: " + rev)
        print(ref)


    def _obtainKey(self, IDpaziente, IDclinica, DdRevoca, DdReferto):
        paziente = IDpaziente
        clinica = IDclinica
        ksim, krev =  DdReferto[0], DdRevoca[0]
        if ksim is not None:
            ksim = PiAsim.DecAsim(self._kpriv, ksim)
        if krev is not None:
            krev = PiAsim.DecAsim(self._kpriv, krev)

        return ksim, krev


    def _ref_request(self, IDpaziente, IDreferto, auth):
        message = [self._ID, oc.REF_REQ, IDpaziente, IDreferto, auth]
        IDrm = self._ca.getRMID()
        self.send(IDrm, message)

    def _receiveKey(self, message):
        print("Operazione non valida")
        return

    def _aud_request(self, IDpaziente, IDreferto, auth):
        message = [self._ID, oc.AUD_REQ, IDpaziente, IDreferto, auth]
        IDrm = self._ca.getRMID()
        self.send(IDrm, message)





