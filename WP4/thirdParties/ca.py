from users import Role
from thirdParties.comunicationChannel import ComunicationChannel
#Certificate Authority
class CA:

    #inizializzazione del database degli utenti
    def __init__(self):
        self.pdict = dict()
        self.cdict = dict()
        self.mdict = dict()
        self._cc = ComunicationChannel()
        self._rm = None



    def subscribe(self, actor, role, kpub):
        #Controllo sulla chiave pubblica dell'utente
        if kpub == None:
            raise ValueError

        if role == Role.RM:
            ID = "RM0"
            self._rm = (ID, actor._role, actor._kpub)
        elif role == Role.CLINICA:
            ID = "C" + len(self.cdict)
            self.cdict[ID] = (kpub, role)
        elif role == Role.PAZIENTE:
            ID = "P" + len(self.pdict)
            self.pdict[ID] = (kpub, role)
        elif role == Role.MEDICO:
            ID = "M" + len(self.mdict)
            self.mdict[ID] = (kpub, role)
        else:
            raise ValueError
        self._cc._add(ID, actor)
        actor._cc = self._cc
        return ID

    def getPublic(self, ID):
        r = ID[0]
        if ID == self._rm[0]:
            return self._rm[2]
        elif r == "C":
            return self.cdict[ID][0]
        elif r == "P":
            return self.pdict[ID][0]
        elif r == "M":
            return self.mdict[ID][0]
        else:
            raise ValueError

    def getRole(self,ID):
        r = ID[0]
        if ID == self.rm[0]:
            return [2]
        elif r == "C":
            return self.cdict[ID][1]
        elif r == "P":
            return self.pdict[ID][1]
        elif r == "M":
            return self.mdict[ID][1]
        else:
            raise ValueError

