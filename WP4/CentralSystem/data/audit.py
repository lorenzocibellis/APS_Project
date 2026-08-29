import pickle

from cryptoOperation.serializer import Serializer


class Audit:
    def __init__(self, IDrichiedente, operation, cnt, signaudit):
        self.IDrichiedente = IDrichiedente
        self.operation = operation
        self.cnt = cnt
        self.signaudit = signaudit

    def serialize(self):
        return Serializer.serialize(self)

    def deserialize(serializedAudit):
        return Serializer.deserialize(serializedAudit)