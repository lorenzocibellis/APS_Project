from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.fernet import Fernet

class piSim:
    def genSim():
        return Fernet.generate_key()

    def encSim(k , plain):
        f = Fernet(k)
        cipher = f.encrypt(plain)
        return cipher

    def decSim(k , cipher):
        f = Fernet(k)
        plain = f.decrypt(cipher)
        return plain



class piAsim:
    def genAsim(n = 2048):
        priv = rsa.generate_private_key(
            public_exponent = 65537,
            key_size = n
        )
        pub = priv.public_key()
        return priv,pub

    def encAsim(k , plain):
        cipher = k.encrypt(
            plain,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return cipher

    def decAsim(k , cipher):
        plain = k.decrypt(
            cipher,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plain


class H:
    def Hash(value):
        return

    def HVrfy(value, hash):
        return

class S:
    def Sign(k, value):
        return

    def Vrfy(k, value, sign):
        return