from cryptoOperation.cryptOp import PiAsim
from interfaces import Comunication
from users import Role

class RM(Comunication):

    def receive(self, c):
        m , op , audit , signaudit = super().receive(c)
        if op == "00":
            self.store(m, audit, signaudit)
        elif op == "01":
            self.getRef(m, audit, signaudit)
        elif op == "05":
            self.getKey(m,audit,signaudit)
        elif op == "07":
            self.revoke(m,audit,signaudit)
        elif op == "08":
            self.revoke(m,audit,signaudit)
        elif op == "09":
            self.getAuditing(m,audit,signaudit)
        else:
            ValueError("Codice non valido")

        print("Richiesta elaborata")




    def store(self, m, audit, signaudit):
            if len(m) != 5:
                raise ValueError("Lunghezza del pacchetto errata")
            print(m)
            IDclinica, _ , IDpaziente , IDreferto, DdR = m
            ksimc, ksimp , trev, creferto = DdR
