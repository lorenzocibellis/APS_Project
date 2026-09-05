import pickle

from cryptoOperation.serializer import Serializer
from cryptoOperation.cryptOp import PiAsim
from thirdParties.ca import CA


class Audit:
    def __init__(self, IDrichiedente, operation, cnt, signaudit):
        self._IDrichiedente = IDrichiedente
        self._operation = operation
        self._cnt = cnt
        self._signaudit = signaudit

    def serialize(self):
        return Serializer.serialize(self)

    @staticmethod
    def deserialize(serializedAudit):
        return Serializer.deserialize(serializedAudit)

    def getID(self):
        return self._IDrichiedente

    def getOp(self):
        return self._operation

    def getCnt(self):
        return self._cnt

    def getSign(self):
        return self._signaudit

    def getAll(self):
        return [self.getID(), self.getOp(), self.getCnt(), self.getSign()]


    def __str__(self):
        s = "ID richiedente: " + self._IDrichiedente +\
              "\nOperazione effettuata: " + str(self._operation) +\
              "\nValore del contatore: " + str(self._cnt) +\
              "\nFirma: " + str(self._signaudit)
        return s