from enum import StrEnum


class Role(StrEnum):
    CLINICA = "Clinica"
    PAZIENTE = "Paziente"
    MEDICO = "Medico"
    RM = "Request Manager"


class OperationCode(StrEnum):
    STORE = "00"
    REF_REQ = "01"
    SEND = "02"
    VIS_REQ = "03"
    CONFIRM = "04"
    KEY_REQ = "05"
    KEY_SEND = "06"
    REVOKE = "07"
    UPDATE = "08"
    AUD_REQ = "09"
    AUD_SEND = "10"
    NOTIFY = "11"

class NotifyCode(StrEnum):
    SUCCESS = "00"
    INVALID_DATA = "01"
    UNAUTH = "02"
    INEX = "03"
    INVALID_OP = "04"
