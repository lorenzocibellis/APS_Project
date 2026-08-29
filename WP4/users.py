from enum import StrEnum
from interfaces import Comunication
from cryptoOperation.cryptOp import PiAsim

class Role(StrEnum):
    CLINICA = "Clinica"
    PAZIENTE = "Paziente"
    MEDICO = "Medico"
    RM = "Request Manager"


class User(Comunication):
    _role = None
    _ID = None
    _kpriv = None
    _kpub = None
    _identity = False

    def __init__(self, role):
        self._role = role

    #inizializzazione identità presso una CA
    def obtainIdentity(self,ca):
        if not self._identity:

            self._kpriv , self._kpub = PiAsim.GenAsim(2048)
            self._ID = ca.subscribeUser(self , self._role , self._kpub)
            self._identity = True
            return
        print("Identità già inizializzata")



class Clinica(User):


class Paziente(User):


class Medico(User):