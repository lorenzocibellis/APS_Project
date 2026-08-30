from globalClasses.enumerations import Role
from users.userInterface import User


class Paziente(User):
    def __init__(self, ca, rm):
        super().__init__(Role.PAZIENTE, ca, rm)