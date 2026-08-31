from CentralSystem.data.register import Register

class Item:
    def __init__(self, IDpaziente, IDreferto, IDclinica, ksimpaziente, ksimclinica, krevpaziente, krevclinica, trev, CdR,crevoca, creferto):
        self._IDpaziente = IDpaziente
        self._IDreferto = IDreferto
        self._IDclinica = IDclinica
        self._ksimpaziente = ksimpaziente
        self._ksimclinica = ksimclinica
        self._krevpaziente = krevpaziente
        self._krevclinica = krevclinica
        self._flagRevoca = False
        self._trev = trev
        self._CdR = CdR
        self._crevoca = crevoca
        self._creferto = creferto
        self._register = Register()
        return

    def revokeItem(self, krevpaziente, krevclinica, trev, CdR, crevoca):
        self._krevpaziente = krevpaziente
        self._krevclinica = krevclinica
        self._flagRevoca = True
        self._trev = trev
        self._CdR = CdR
        self._crevoca = crevoca
        return

    def updateItem(self, ksimpaziente, ksimclinica, trev, creferto):
        self._ksimpaziente = ksimpaziente
        self._ksimclinica = ksimclinica
        self._flagRevoca = False
        self._trev = trev
        self._creferto = creferto
        return

    def addAudit(self, audit):
        self._register.addAudit(audit)

    def isRevoked(self):
        return self._flagRevoca

    def getCdR(self):
        return self._CdR

    def getIDpaziente(self):
        return self._IDpaziente

    def getIDclinica(self):
        return self._IDclinica

    def getIDreferto(self):
        return self._IDreferto

    def getTokenRev(self):
        return self._trev

    def getCdR(self):
        return self._CdR

    def getMdr(self):
        return self._crevoca

    def getReferto(self):
        return self._creferto

    def getKeyClinica(self):
        return self._ksimclinica, self._krevclinica

    def getKeyPaziente(self):
        return self._ksimpaziente, self._krevpaziente

    def __str__(self):
        stato_revoca = "REVOCATO" if self._flagRevoca else "ATTIVO"

        return (
            f"=== Item Referto [{self._IDreferto}] ===\n"
            f"  • Paziente ID:       {self._IDpaziente}\n"
            f"  • Clinica ID:        {self._IDclinica}\n"
            f"  • Stato:             {stato_revoca}\n"
            f"  • Token validazione Revoca:  {self._trev}\n"
            f"  • KSim Paziente:     {self._ksimpaziente}\n"
            f"  • KSim Clinica:      {self._ksimclinica}\n"
            f"  • KRev Paziente:     {self._krevpaziente}\n"
            f"  • KRev Clinica:      {self._krevclinica}\n"
            f"  • Cifrato Referto:   {self._creferto}\n"
            f"  • Cifrato Revoca:    {self._crevoca}\n"
            f"  • Codice della Revoca:    {self._CdR}\n"
            f"  • Registro Audit:    {self._register}\n"
            f"================================="
        )