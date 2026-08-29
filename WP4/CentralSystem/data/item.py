from CentralSystem.data.register import Register

class Item:
    def __init__(self, IDclinica, ksimpaziente, ksimclinica, krevpaziente, krevclinica, trev, crevoca, creferto):
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
