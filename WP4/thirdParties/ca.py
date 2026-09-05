from globalClasses.enumerations import Role
from thirdParties.comunicationChannel import ComunicationChannel


#Certificate Authority
class CA:

    #inizializzazione del database degli utenti
    def __init__(self):
        self._pdict = dict()
        self._cdict = dict()
        self._mdict = dict()
        self._cc = ComunicationChannel()
        self._rm = None



    def subscribe(self, actor, role, kpub):
        #Controllo sulla chiave pubblica dell'utente
        if kpub == None:
            raise ValueError

        if role == Role.RM:
            if self._rm is None:
                ID = "RM0"
                self._rm = (ID, actor._role, actor._kpub)
            else:
                print("RM già inizializzato")
        elif role == Role.CLINICA:
            ID = "C" + str(len(self._cdict))
            self._cdict[ID] = (kpub, role)
        elif role == Role.PAZIENTE:
            ID = "P" + str(len(self._pdict))
            self._pdict[ID] = (kpub, role)
        elif role == Role.MEDICO:
            ID = "M" + str(len(self._mdict))
            self._mdict[ID] = (kpub, role)
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
            if ID not in self._cdict:
                return None
            return self._cdict[ID][0]
        elif r == "P":
            if ID not in self._pdict:
                return None
            return self._pdict[ID][0]
        elif r == "M":
            if ID not in self._mdict:
                return None
            return self._mdict[ID][0]
        else:
            print("Utente non esistente")
            return None

    def getRole(self,ID):
        r = ID[0]
        if ID == self._rm[0]:
            return self._rm[1]
        elif r == "C":
            if ID not in self._cdict:
                return None
            return self._cdict[ID][1]
        elif r == "P":
            if ID not in self._pdict:
                return None
            return self._pdict[ID][1]
        elif r == "M":
            if ID not in self._mdict:
                return None
            return self._mdict[ID][1]
        else:
            print("Utente non esistente")
            return None

    def getRMID(self):
        return self._rm[0]


