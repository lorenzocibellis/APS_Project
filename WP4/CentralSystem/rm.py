from interfaces import Comunication
from users import Role

class RM(Comunication):
    _role = None
    _ID = None
    _kpriv = None
    _kpub = None

    def __init__(self, ca):
        self._role = Role.RM
        self._kpriv, self._kpub = PiAsim.GenAsim(2048)
        self._ID = ca.subscribeRM(self, self._kpub)
        return