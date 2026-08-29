#implementazione serializzazione e deserializzazione
import pickle


class Serializer:

    @staticmethod
    def serialize(itemToSerialize):
        return pickle.dumps(itemToSerialize)

    @staticmethod
    def deserialize(serializedItem):
        return pickle.loads(serializedItem)