from cryptoOperation.cryptOp import H
from cryptoOperation.serializer import Serializer

class Register:
    def __init__(self):
        self._register = []
        self._g = None

    def addAudit(self, a, IDpaziente, IDreferto):
        if a is None:
            raise ValueError
        l = len(self._register)
        if l == 0:
            base = [IDpaziente, IDreferto]
            self._g = H.Hash(Serializer.serialize(base))
            self._register.append((a, H.Hash(a.serialize() + b"|" + self._g)))
        else:
            self._register.append((a, H.Hash(a.serialize() + b"|" + self._register[l - 1][1])))

    def getAudit(self, index):
        if index >= len(self._register):
            print("Index Out Of Bounds")
            return None, None

        return self._register[index]

    def getGenesis(self):
        return self._g

    def __len__(self):
        return len(self._register)


    def serialize(self):
        return Serializer.serialize(self)

    @staticmethod
    def deserialize(serializedRegister):
        return Serializer.deserialize(serializedRegister)

    def __str__(self):
        s = "REGISTRO:\nGenesis: " + str(self._g) + "\n"
        i = 0
        for (audit, hash) in self._register:
            s = s + "\nAudit " + str(i) + ": \n" + str(audit) + "\nHash: " + str(hash) + "\n"
            i += 1
        return s




