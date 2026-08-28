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

    #inizializzazione identità presso una CA
    def obtainIdentity(self,ca):
        if not self._identity:
            self.kpriv = rsa.generate_private_key(
                key_size=2048,
                public_exponent=65537
            )
            self.kpub = self.kpriv.public_key()
            self.id = ca.subscribeUser(self , self._role , self._kpub)
            self._identity = True
            return
        print("Identità già inizializzata")


