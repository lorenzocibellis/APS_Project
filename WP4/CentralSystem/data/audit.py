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


    _opDesc = {
        "00": "Caricamento Referto",
        "01": "Richiesta Referto",
        "02": "Invio Referto",
        "03": "Richiesta Visualizzazione",
        "04": "Conferma Visualizzazione",
        "05": "Richiesta Chiavi",
        "06": "Invio Chiavi",
        "07": "Revoca Referto",
        "08": "Aggiornamento Referto",
        "09": "Richiesta Auditing",
        "10": "Invio Auditing",
        "11": "Notifica",
    }

    def __str__(self):
        opCode = str(self._operation)
        desc = self._opDesc.get(opCode, "")
        opDisplay = f"{opCode} ({desc})" if desc else opCode

        s = "ID richiedente: " + self._IDrichiedente +\
              "\nOperazione effettuata: " + opDisplay +\
              "\nValore del contatore: " + str(self._cnt) +\
              "\nFirma: " + str(self._signaudit)
        return s