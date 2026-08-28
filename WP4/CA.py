from Users import Role

#Certificate Authority
class CA:

    #inizializzazione del database degli utenti
    def __initialite__(self):
        self.pdict = dict()
        self.cdict = dict()
        self.mdict = dict()


    def subscribeUser(self, user, role, kpub):
        #Controllo sulla chiave pubblica dell'utente
        if kpub == None:
            raise ValueError

        if role == Role.CLINICA:
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
        return ID

    def getPublic(self, ID):
        r = ID[0]
        if r == "C":
            return self.cdict[ID][0]
        elif r == "P":
            return self.pdict[ID][0]
        elif r == "M":
            return self.mdict[ID][0]
        else:
            raise ValueError

    def getRole(self,ID):
        r = ID[0]
        if r == "C":
            return self.cdict[ID][1]
        elif r == "P":
            return self.pdict[ID][1]
        elif r == "M":
            return self.mdict[ID][1]
        else:
            raise ValueError
