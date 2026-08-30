from datetime import timezone, datetime, timedelta

from cryptoOperation.cryptOp import S
from cryptoOperation.serializer import Serializer
from interfaces import Comunication
from CentralSystem.data.database import Database
from globalClasses.enumerations import OperationCode as oc, NotifyCode as nc, Role


class RM(Comunication):

    _daysToExpire = 2

    def __init__(self, role, ca, db: Database):
        super().__init__(role, ca)
        self._db = db


    def receive(self, c):
        data = super().receive(c)
        if data is None:
            return
        m, sender, op, kpub, cnt, signaudit = data
        print("Elaborazione della richiesta")
        if op == oc.STORE:
            #controllo sincronizzazione dati tra mittente e messaggio
            if self._ca.getRole(sender) != Role.CLINICA or sender != m[0]:
                self._notifyMessage(sender, nc.INVALID_DATA)
                return

            self._store(m, cnt, signaudit)

        elif op == oc.REF_REQ:
            self._getRef(m, cnt, signaudit)

        elif op == oc.KEY_REQ:
            self._getKey(m, cnt, signaudit)

        elif op == oc.REVOKE:
            self._revoke(m, cnt, signaudit)

        elif op == oc.UPDATE:
            self._update(m, cnt, signaudit)

        elif op == oc.AUD_REQ:
            self._getAuditing(m, cnt, signaudit)

        else:
            self._notifyMessage(sender ,nc.INVALID_OP)

        print("RM : Richiesta elaborata")



    def _store(self, m, cnt ,signaudit):
        if len(m) != 5:
           self._notifyMessage(m[0], nc.INVALID_DATA)
           return
        print(m)
        IDclinica, _ , IDpaziente , IDreferto, DdR = m
        ksimc, ksimp , trev, creferto = DdR
        error = self._db.addItem(IDpaziente, IDreferto, IDclinica, ksimp, ksimc, None, None, trev, None, creferto)
        if error == nc.SUCCESS:
            self._db.addAudit(IDpaziente, IDreferto, IDclinica, oc.STORE, cnt, signaudit)
        self._notifyMessage(IDclinica ,error)


    def _getRef(self, m, cnt, signaudit):
        if len(m) != 5:
            self._notifyMessage(m[0], nc.INVALID_DATA)
            return
        print("RM: Elaborazione Caricamento Referto")
        print(m)
        IDrichiedente, _, IDpaziente, IDreferto, Auth = m

        #Controllo che il referto esista in memoria
        if not self._db.exists(IDpaziente,IDreferto):
            self._notifyMessage(IDrichiedente, nc.INEX)
            return

        role = self._ca.getRole(IDrichiedente)

        IDclinica = self._db.getIDclinica(IDpaziente, IDreferto)
        #CASO SPECIALE: autorizzazione per il medico
        if role == Role.MEDICO:
            print("RM: Controllo autorizzazione per medico " + IDrichiedente)
            sign, IDmedico, IDpazienteAuth, IDrefertoAuth, TimeStamp = Auth

            #controllo sincronizzazione dati
            if IDmedico != IDrichiedente or IDpazienteAuth != IDpaziente or IDrefertoAuth != IDreferto:
                self._notifyMessage(IDrichiedente, nc.INVALID_DATA)
                return

            #controllo scadenza autorizzazione
            if not isinstance(TimeStamp, datetime):
                self._notifyMessage(IDrichiedente, nc.INVALID_DATA)
                return
            if  TimeStamp + timedelta(days = self._daysToExpire) < datetime.now(timezone.utc):
                self._notifyMessage(IDrichiedente, nc.UNAUTH)
                return

            # controllo autorizzazione
            kpub = self._ca.getPublic(IDpaziente)
            if not S.Vrfy(kpub, Serializer.serialize(Auth[1:]), sign):
                self._notifyMessage(IDrichiedente, nc.UNAUTH)
                return

            print("RM: Autorizzazione consentita a :" + IDrichiedente)

        # Si controlla che chi ha richiesto i documenti sia autorizzato ad ottenerli
        elif IDrichiedente != IDpaziente and IDrichiedente != IDclinica:
                self._notifyMessage(IDrichiedente, nc.UNAUTH)
                return

        #si aggiunge l'evento al registro audit
        self._db.addAudit(IDpaziente, IDreferto, IDclinica, oc.REF_REQ, cnt, signaudit)

        self._sendReferto(IDpaziente, IDreferto, IDrichiedente)
        return


    def _sendReferto(self, IDpaziente, IDreferto, receiver):
        item = self._db.getItem(IDpaziente, IDreferto)
        print("RM: Preparazione messaggio di invio del referto")
        op = oc.REF_SEND
        sender = self._ID
        IDclinica = item.getIDclinica()
        IDpaziente = item.getIDpaziente()
        flag = item.isRevoked()

        #decisione sulle chiavi
        if receiver == IDpaziente:
            ksim, krev = item.getKeyPaziente()
        elif receiver == item.getIDclinica():
            ksim,krev = item.getKeyClinica()
        else:
            #il receiver è un dottore
            #Dummy bits per il medico
            ksim, krev = None , None

        trev = item.getTokenRev()
        crevoca = item.getMdr()
        DdRevoca = [krev, trev, crevoca]

        creferto = item.getReferto()
        DdReferto = [ksim, creferto]

        #combinazione dati nel messaggio
        message = [sender, receiver, op, IDclinica, IDpaziente, flag, DdRevoca, DdReferto]

        print("RM: Messaggio creato")
        self.send(receiver, message)
        return

    def _notifyMessage(self, receiver, code):
        message = [self._ID, oc.NOTIFY, code]
        print("RM : Invio messaggio di risposta")
        self.send(receiver, message)
