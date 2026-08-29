#from CentralSystem.rm import RM
from CentralSystem.data.audit import Audit
from CentralSystem.data.item import Item

class Database:

    def __init__(self):
        self._database = dict()

    def addItem(self, IDpaziente, IDreferto, IDclinica, ksimpaziente, ksimclinica, krevpaziente, krevclinica,trev, crevoca, creferto , verbose = False):
        item = Item(IDpaziente, IDreferto, IDclinica, ksimpaziente, ksimclinica, krevpaziente, krevclinica, trev, crevoca, creferto)
        if item in self:
            return "01"
        if IDpaziente not in self._database:
            self._database[IDpaziente] = dict()
        self._database[IDpaziente][IDreferto] = item

        #modalità verbose
        if verbose:
            print("\nAggiunto item:\n" + str(item) +"\n")
        return "00"

    def revokeItem(self, IDpaziente, IDreferto, krevpaziente, krevclinica, trev, crevoca):
        if IDpaziente not in self._database:
            return "03"
        if IDreferto not in self._database[IDpaziente]:
            return "03"
        self._database[IDpaziente][IDreferto].revokeItem(krevpaziente, krevclinica, trev, crevoca)
        return "00"


    def updateItem(self, IDpaziente, IDreferto, ksimpaziente, ksimclinica, trev, creferto):
        if IDpaziente not in self._database:
            return "03"
        if IDreferto not in self._database[IDpaziente]:
            return "03"
        self._database[IDpaziente][IDreferto].updateItem(ksimpaziente, ksimclinica, trev, creferto)
        return "00"

    def addAudit(self,IDpaziente,IDreferto,ID, op, cnt, signaudit ):
        item = self._database[IDpaziente][IDreferto]
        item.addAudit( Audit(ID, op, cnt, signaudit) )

    def getItem(self, IDpaziente, IDreferto):
        return self._database[IDpaziente][IDreferto]

    def getRM(self):
        return self.rm

    def isRevoked(self, IDpaziente, IDreferto):
        if IDpaziente not in self._database:
            return False
        if IDreferto not in self._database[IDpaziente]:
            return False
        return self._database[IDpaziente][IDreferto].isRevoked()

    def __contains__(self, item):
        p , r = item.getIDpaziente() , item.getIDreferto()
        if p not in self._database:
            return False
        if r not in self._database[p]:
            return False
        return self._database[p][r] is not None


