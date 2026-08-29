class ComunicationChannel:

    def __init__(self):
        self._channel = dict()

    def _add(self, ID, actor):
        self._channel[ID] = actor

    def get(self, ID):
        if ID in self._channel:
            return self._channel[ID]
        raise ValueError("L'ID non è presente nel sistema")

    def send(self,ID,message):
        self._channel[ID].receive(message)