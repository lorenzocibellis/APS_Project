from enum import StrEnum
from Comunication import Comunication
from cryptography.hazmat.primitives.asymmetric import rsa

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

    def obtainIdentity(self,ca):
        if not self._identity:

            self.id = ca.subscribeUser(self , self._role , self._kpub)
