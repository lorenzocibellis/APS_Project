from cryptoOperation.cryptOp import H

#implementazione serializzazione e deserializzazione
import pickle

class Register:
    def __init__(self, genesis=b"0000"):
        self._register = []
        self.g = genesis

    def addAudit(self, a):
        if a is None:
            raise ValueError
        l = len(self._register)
        if l == 0:
            self._register.append((a, H.Hash(a.serialize() + b"|" + self.g)))
        else:
            self._register.append((a, H.Hash(a.serialize() + b"|" + self._register[l - 1][1])))

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(serializedRegister):
        return pickle.loads(serializedRegister)




