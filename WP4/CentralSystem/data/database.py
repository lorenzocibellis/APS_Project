#from CentralSystem.rm import RM
from CentralSystem.data.item import Item

class Database:

    def _addItem(self, IDpaziente, IDreferto, IDclinica, ksimpaziente, ksimclinica, krevpaziente, krevclinica,trev, crevoca, creferto):
        item = Item(IDclinica, ksimpaziente, ksimclinica, krevpaziente, krevclinica, trev, crevoca, creferto)
        if IDpaziente not in self._database:
            self._database[IDpaziente] = dict()
        if IDreferto in self._database:
            raise ValueError
        self._database[IDpaziente][IDreferto] = item
        return

    def _revokeItem(self, IDpaziente, IDreferto, krevpaziente, krevclinica, trev, crevoca):
        if IDpaziente not in self._database:
            raise ValueError
        if IDreferto not in self._database[IDpaziente]:
            raise ValueError
        self._database[IDpaziente][IDreferto].revokeItem(krevpaziente, krevclinica, trev, crevoca)
        return


    def _updateItem(self, IDpaziente, IDreferto, ksimpaziente, ksimclinica, trev, creferto):
        if IDpaziente not in self._database:
            raise ValueError
        if IDreferto not in self._database[IDpaziente]:
            raise ValueError
        self._database[IDpaziente][IDreferto].updateItem(ksimpaziente, ksimclinica, trev, creferto)
        return

    def getRM(self):
        return self.rm

