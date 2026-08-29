import pickle

class Audit:
    def __init__(self, IDrichiedente, operation, cnt, signaudit):
        self.IDrichiedente = IDrichiedente
        self.operation = operation
        self.cnt = cnt
        self.signaudit = signaudit

    def serialize(self):
        return pickle.dumps(self)

    def deserialize(serializedAudit):
        return pickle.loads(serializedAudit)