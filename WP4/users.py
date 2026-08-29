from enum import StrEnum
from interfaces import Comunication


class Role(StrEnum):
    CLINICA = "Clinica"
    PAZIENTE = "Paziente"
    MEDICO = "Medico"
    RM = "Request Manager"



#class Clinica(Comunication):


#class Paziente(Comunication):


#class Medico(Comunication):