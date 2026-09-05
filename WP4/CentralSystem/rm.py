from datetime import timezone, datetime, timedelta
from io import UnsupportedOperation

from cryptoOperation.cryptOp import S
from cryptoOperation.serializer import Serializer
from comunicationInterface import Comunication
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
        if len(data) != 6:
            return
        m, sender, op, kpub, cnt, signaudit = data

        # controllo sincronizzazione dati tra mittente e messaggio
        if sender != m[0]:
            self._notifyMessage(sender, nc.INVALID_DATA)
            return

        print(self._ID + ": Elaborazione della richiesta")
        if op == oc.STORE:

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

        print("RM: Elaborazione caricamento referto")
        IDclinica, _ , IDpaziente , IDreferto, DdR = m
        ksimc, ksimp , trev, CdR ,creferto = DdR

        if self._existentID(IDclinica) is False:
            print("Utente non esistente")
            return

        if self._ca.getRole(IDclinica) != Role.CLINICA:
            self._notifyMessage(IDclinica, nc.UNAUTH)
            return

        #controllo trev
        kpub = self._ca.getPublic(IDclinica)
        if kpub is None:
            self._notifyMessage(IDclinica, nc.INVALID_DATA)
        base = [IDreferto, CdR, False]

        if not S.Vrfy(kpub, Serializer.serialize(base), trev):
            self._notifyMessage(m[0], nc.INVALID_DATA)
            return

        error = self._db.addItem(IDpaziente, IDreferto, IDclinica, ksimp, ksimc, None, None, trev, CdR,None, creferto)
        if error == nc.SUCCESS:
            self._db.addAudit(IDpaziente, IDreferto, IDclinica, oc.STORE, cnt, signaudit)
        self._notifyMessage(IDclinica ,error)


    def _getRef(self, m, cnt, signaudit):
        if len(m) != 5:
            self._notifyMessage(m[0], nc.INVALID_DATA)
            return
        print("RM: Elaborazione Richiesta Referto")
        IDrichiedente, _, IDpaziente, IDreferto, Auth = m

        if self._existentID(IDrichiedente) is False:
            print("Utente non esistente")
            return

        #Controllo che il referto esista in memoria
        if not self._db.exists(IDpaziente,IDreferto):
            self._notifyMessage(IDrichiedente, nc.INEX)
            return

        role = self._ca.getRole(IDrichiedente)
        if role is None:
            self._notify(nc.INVALID_DATA)
            return

        IDclinica = self._db.getIDclinica(IDpaziente, IDreferto)
        #CASO SPECIALE: autorizzazione per il medico
        if role == Role.MEDICO:
            print("RM: Controllo autorizzazione per medico " + IDrichiedente)
            if len(Auth) != 5:
                self._notifyMessage(IDrichiedente, nc.INVALID_DATA)
                return
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
        self._db.addAudit(IDpaziente, IDreferto, IDrichiedente, oc.REF_REQ, cnt, signaudit)

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
        CdR = item.getCdR()
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
        DdRevoca = [krev, trev, CdR, crevoca]

        creferto = item.getReferto()
        DdReferto = [ksim, creferto]

        #combinazione dati nel messaggio
        message = [sender,  op, IDclinica, IDpaziente, IDreferto, flag, DdRevoca, DdReferto]

        print("RM: Messaggio creato")
        self.send(receiver, message)
        return


    def _revoke(self, m, cnt, signaudit):
        if len(m) != 5:
            self._notifyMessage(m[0], nc.INVALID_DATA)
            return

        print("RM: Elaborazione Revoca Referto")
        IDrichiedente, _, IDpaziente, IDreferto, DdR = m


        if self._existentID(IDrichiedente) is False:
            print("Utente non esistente")
            return

        if not self._db.exists(IDpaziente, IDreferto):
            print("Referto non esistente")
            return

        if self._db.isRevoked(IDpaziente, IDreferto):
            self._notifyMessage(IDrichiedente, nc.INVALID_OP)
            return

        if len(DdR) != 5:
            self._notifyMessage(m[0], nc.INVALID_DATA)
            return

        krevc, krevp, trev, CdR, crev = DdR

        #Controllo che la clinica della revoca è la stessa che ha creato il referto
        if not self._db.getIDclinica(IDpaziente,IDreferto) == IDrichiedente:
            self._notifyMessage(IDrichiedente, nc.UNAUTH)
            return

        #controllo trev
        kpub = self._ca.getPublic(IDrichiedente)
        base = [IDreferto, CdR, True]
        if not S.Vrfy(kpub, Serializer.serialize(base), trev):
            self._notifyMessage(m[0], nc.INVALID_DATA)
            return


        error = self._db.revokeItem(IDpaziente, IDreferto, krevp, krevc, trev, CdR, crev)
        if error == nc.SUCCESS:
            self._db.addAudit(IDpaziente, IDreferto, IDrichiedente, oc.REVOKE, cnt, signaudit)
        self._notifyMessage(IDrichiedente ,error)


    def _update(self, m, cnt, signaudit):
        if len(m) != 5:
            self._notifyMessage(m[0], nc.INVALID_DATA)
            return

        print("Elaborazione aggiornamento referto")
        IDrichiedente, _, IDpaziente, IDreferto, DdR = m

        if self._existentID(IDrichiedente) is False:
            print("Utente non esistente")
            return

        if not self._db.exists(IDpaziente, IDreferto):
            print("Referto non esistente")
            return

        if not self._db.isRevoked(IDpaziente, IDreferto):
            self._notifyMessage(IDrichiedente, nc.INVALID_OP)
            return

        if len(DdR) != 4:
            self._notifyMessage(m[0], nc.INVALID_DATA)
            return

        ksimc, ksimp, trev, cref = DdR

        #Controllo che la clinica dell'aggiornamento è la stessa che ha creato il referto
        if not self._db.getIDclinica(IDpaziente,IDreferto) == IDrichiedente:
            self._notifyMessage(IDrichiedente, nc.UNAUTH)
            return

        #controllo trev
        kpub = self._ca.getPublic(IDrichiedente)
        base = [IDreferto, self._db.getCdR(IDpaziente,IDreferto), False]
        if not S.Vrfy(kpub, Serializer.serialize(base), trev):
            self._notifyMessage(m[0], nc.INVALID_DATA)
            return


        error = self._db.updateItem(IDpaziente, IDreferto, ksimp, ksimc, trev, cref)
        if error == nc.SUCCESS:
            self._db.addAudit(IDpaziente, IDreferto, IDrichiedente, oc.UPDATE, cnt, signaudit)
        self._notifyMessage(IDrichiedente ,error)


    def _getKey(self, m, cnt, signaudit):
        if len(m) != 3:
            self._notifyMessage(m[0], nc.INVALID_DATA)
            return

        print("RM: Elaborazione Invio chiavi")

        IDrichiedente, _, IDreferto = m

        if self._existentID(IDrichiedente) is False:
            print("Utente non esistente")
            return

        #Controllo che il richiedente sia un paziente
        if self._ca.getRole(IDrichiedente) is None or self._ca.getRole(IDrichiedente) != Role.PAZIENTE:
            self._notifyMessage(IDrichiedente, nc.UNAUTH)
            return

        #Controllo che il referto esista in memoria
        #ciò vale anche per ottenere il referto associato al richiedente
        if not self._db.exists(IDrichiedente,IDreferto):
            self._notifyMessage(IDrichiedente, nc.INEX)
            return

        #si aggiunge l'evento al registro audit
        self._db.addAudit(IDrichiedente, IDreferto, IDrichiedente, oc.KEY_REQ, cnt, signaudit)

        #si inviano le chiavi
        self._sendKeys(IDrichiedente, IDreferto)
        return


    def _sendKeys(self, IDpaziente, IDreferto):
        print("RM: Preparazione messaggio di invio delle chiavi")
        op = oc.KEY_SEND
        sender = self._ID

        ksim, krev = self._db.getKeyPaziente(IDpaziente, IDreferto)

        # combinazione dati nel messaggio
        message = [sender, op, IDpaziente, IDreferto, krev, ksim]

        print("--RM: Messaggio creato--")
        self.send(IDpaziente, message)
        return

    def _getAuditing(self, m, cnt, signaudit):
        if len(m) != 5:
            self._notifyMessage(m[0], nc.INVALID_DATA)
            return

        print("RM: Elaborazione Richiesta Auditing")
        

        IDrichiedente, _, IDpaziente, IDreferto, Auth = m

        if self._existentID(IDrichiedente) is False:
            print("Utente non esistente")
            return

        role = self._ca.getRole(IDrichiedente)
        if role is None:
            return

        #Controllo che il referto esista in memoria
        if not self._db.exists(IDpaziente,IDreferto):
            self._notifyMessage(IDrichiedente, nc.INEX)
            return



        IDclinica = self._db.getIDclinica(IDpaziente, IDreferto)
        #CASO SPECIALE: autorizzazione per il medico
        if role == Role.MEDICO:
            print("RM: Controllo autorizzazione per medico " + IDrichiedente)
            if len(Auth) != 5:
                self._notifyMessage(IDrichiedente, nc.INVALID_DATA)
                return
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


        # Si controlla che chi ha richiesto il registro sia autorizzato ad ottenerli
        elif IDrichiedente != IDpaziente and IDrichiedente != IDclinica:
                self._notifyMessage(IDrichiedente, nc.UNAUTH)
                return

        #si aggiunge l'evento al registro audit
        self._db.addAudit(IDpaziente, IDreferto, IDrichiedente, oc.AUD_REQ, cnt, signaudit)

        self._sendAudit(IDpaziente, IDreferto, IDrichiedente)
        return


    def _sendAudit(self, IDpaziente, IDreferto, receiver):
        register = self._db.getItem(IDpaziente, IDreferto).getRegister()
        print("RM: Preparazione messaggio di invio del registro di auditing")
        op = oc.AUD_SEND
        sender = self._ID

        # combinazione dati nel messaggio
        message = [sender, op, IDpaziente, IDreferto, register]

        print("RM: Messaggio creato")
        self.send(receiver, message)
        return


    def _notifyMessage(self, receiver, code):
        message = [self._ID, oc.NOTIFY, code]
        print("RM : Invio messaggio di risposta")
        self.send(receiver, message)
