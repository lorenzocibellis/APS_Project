from CentralSystem.data.register import Register

class Item:
    def __init__(self, IDpaziente, IDreferto, IDclinica, ksimpaziente, ksimclinica, krevpaziente, krevclinica, trev, crevoca, creferto):
        self._IDpaziente = IDpaziente
        self._IDreferto = IDreferto
        self._clinica = IDclinica
        self._ksimpaziente = ksimpaziente
        self._ksimclinca = ksimclinica
        self._krevpaziente = krevpaziente
        self._krevclinica = krevclinica
        self._flagRevoca = False
        self._trev = trev
        self._crevoca = crevoca
        self._creferto = creferto
        self._register = Register()
        return

    def revokeItem(self, krevpaziente, krevclinica, trev, crevoca):
        self._krevpaziente = krevpaziente
        self._krevclinica = krevclinica
        self._flagRevoca = True
        self._trev = trev
        self._crevoca = crevoca
        return

    def updateItem(self, ksimpaziente, ksimclinica, trev, creferto):
        self._ksimpaziente = ksimpaziente
        self._ksimclinica = ksimclinica
        self._flagRevoca = False
        self._trev = trev
        self._creferto = creferto
        return

    def isRevoked(self):
        return self._flagRevoca

    def getIDpaziente(self):
        return self._IDpaziente

    def getIDclinica(self):
        return self._IDclinica

    def getIDreferto(self):
        return self._IDreferto

    def addAudit(self,audit, signaudit):
        self._register.addAudit(audit, signaudit)
