from cryptoOperation.cryptOp import PiAsim
from interfaces import Comunication
from CentralSystem.data.database import Database

class RM(Comunication):


    def __init__(self, role, ca, db):
        super().__init__(role, ca)
        self._db = db


    def receive(self, c):
        m , op , kpub, cnt, signaudit = super().receive(c)
        if op == "00":
            message = self.store(m, cnt, signaudit)
        elif op == "01":
            self.getRef(m, cnt, signaudit)
        elif op == "05":
            self.getKey(m, cnt, signaudit)
        elif op == "07":
            self.revoke(m, cnt, signaudit)
        elif op == "08":
            self.revoke(m, cnt, signaudit)
        elif op == "09":
            self.getAuditing(m, cnt, signaudit)
        else:
            ValueError("Codice non valido")

        print("Richiesta elaborata")



    def store(self, m, cnt ,signaudit):
        if len(m) != 5:
           raise ValueError("Lunghezza del pacchetto errata")
        print(m)
        IDclinica, _ , IDpaziente , IDreferto, DdR = m
        ksimc, ksimp , trev, creferto = DdR
        error = self._db._addItem(IDpaziente, IDreferto, IDclinica, ksimp, ksimc, None, None ,trev, None, creferto)
        if error is "00":
            self._db.addAudit(IDpaziente, IDreferto, IDclinica, "00", cnt, signaudit)
        return self._noteMessage(m[0], error)




    def _noteMessage(self,dest , code):
        return [dest , "11" , code]

