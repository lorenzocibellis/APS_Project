from CentralSystem.data.audit import Audit
from CentralSystem.data.item import Item
from globalClasses.enumerations import NotifyCode as nc

class Database:

    def __init__(self):
        self._database = dict()

    def addItem(self, IDpaziente, IDreferto, IDclinica, ksimpaziente, ksimclinica, krevpaziente, krevclinica,trev, CdR,crevoca, creferto):
        item = Item(IDpaziente, IDreferto, IDclinica, ksimpaziente, ksimclinica, krevpaziente, krevclinica, trev, CdR ,crevoca, creferto)
        if item in self:
            return nc.INVALID_DATA
        if IDpaziente not in self._database:
            self._database[IDpaziente] = dict()
        self._database[IDpaziente][IDreferto] = item

        return nc.SUCCESS

    def revokeItem(self, IDpaziente, IDreferto, krevpaziente, krevclinica, trev, CdR, crevoca):
        if not self.exists(IDpaziente, IDreferto):
            return nc.INEX
        self._database[IDpaziente][IDreferto].revokeItem(krevpaziente, krevclinica, trev, CdR, crevoca)
        return nc.SUCCESS


    def updateItem(self, IDpaziente, IDreferto, ksimpaziente, ksimclinica, trev, creferto):
        if not self.exists(IDpaziente, IDreferto):
            return nc.INEX
        self._database[IDpaziente][IDreferto].updateItem(ksimpaziente, ksimclinica, trev, creferto)
        return nc.SUCCESS

    def addAudit(self,IDpaziente,IDreferto, IDrichiedente, op, cnt, signaudit ):
        item = self._database[IDpaziente][IDreferto]
        item.addAudit( Audit(IDrichiedente, op, cnt, signaudit), IDpaziente, IDreferto )

    def getItem(self, IDpaziente, IDreferto):
        return self._database[IDpaziente][IDreferto]

    def getRevoca(self, IDpaziente, IDreferto):
        return self.getItem(IDpaziente,IDreferto).getMdr()

    def getReferto(self, IDpaziente, IDreferto):
        return self.getItem(IDpaziente,IDreferto).getReferto()

    def getKeyClinica(self, IDpaziente, IDreferto):
        return self.getItem(IDpaziente, IDreferto).getKeyClinica()

    def getKeyPaziente(self, IDpaziente,IDreferto):
        return self.getItem(IDpaziente, IDreferto).getKeyPaziente()

    def getIDclinica(self, IDpaziente,IDreferto):
        return self.getItem(IDpaziente, IDreferto).getIDclinica()

    def getCdR(self, IDpaziente, IDreferto):
        return self.getItem(IDpaziente, IDreferto).getCdR()

    def isRevoked(self, IDpaziente, IDreferto):
        if not self.exists(IDpaziente, IDreferto):
            return False
        return self._database[IDpaziente][IDreferto].isRevoked()

    def exists(self,IDpaziente,IDreferto):
        if IDpaziente not in self._database:
            return False
        return IDreferto in self._database[IDpaziente]

    def __contains__(self, item):
        p , r = item.getIDpaziente() , item.getIDreferto()
        if not self.exists(p, r):
            return False
        return self._database[p][r] is not None


