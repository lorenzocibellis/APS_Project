from Users import Role
from Interfaces import Comunication
from cryptOp import PiAsim
from cryptOp import H
class System:


    def __init__(self):
        self.database = dict()


    def _addElement(self, IDpaziente, IDreferto, IDclinica, ksimpaziente, ksimclinica, krevpaziente, krevclinicq, fdr, trev, crevoca, creferto):
        return


    class Register:
        def __init__(self , genesis = b"0000"):
            self._register = []
            self.g = genesis

        def addAudit(self, a):
            if len(self._register) == 0:
                self._register.append( (a , a.serialize + b"|" + g) )


        class Audit:
            def __init__(self, IDrichiedente, operation, cnt, signaudit):
                self.IDrichiedente = IDrichiedente
                self.operation = operation
                self.cnt = cnt
                self.signaudit = signaudit

            def serialize(self):
                return


    class Item:
        def __init__(self, IDpaziente, IDreferto, IDclinica, ksimpaziente, ksimclinica, krevpaziente, krevclinica, fdr, trev, crevoca, creferto):
            self.paziente = IDpaziente
            self.referto = IDreferto
            self.clinica = IDclinica
            self.ksimpaziente  = ksimpaziente
            self.ksimclinca = ksimclinica
            self.krevpaziente = krevpaziente
            self.krevclinica = krevclinica
            self.flagRevoca = fdr
            self.trev = trev
            self.crevoca = crevoca
            self.creferto = creferto
            self.register = Register()

    class RM(Comunication):
        _role = None
        _ID = None
        _kpriv = None
        _kpub = None

        def __init__(self, ca):
            self._role = Role.RM
            self._kpriv, self._kpub = PiAsim.GenAsim(2048)
            self._ID = ca.subscribeRM(self, self._kpub)