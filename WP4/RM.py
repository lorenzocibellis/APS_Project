from Users import Role
from cryptography.hazmat.primitives.asymmetric import rsa
from Interfaces import Comunication

class RM(Comunication):
    _role = None
    _ID = None
    _kpriv = None
    _kpub = None

    def __init__(self, ca):
        self._role = Role.RM
        self._kpriv = rsa.generate_private_key()
        self._kpub = self._kpriv.public_key()
        self._ID = ca.subscribeRM(self, self._kpub)

