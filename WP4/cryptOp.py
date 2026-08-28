from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.fernet import Fernet

class PiSim:
    def GenSim():
        return Fernet.generate_key()

    def EncSim(k , plain):
        f = Fernet(k)
        cipher = f.encrypt(plain)
        return cipher

    def DecSim(k , cipher):
        f = Fernet(k)
        plain = f.decrypt(cipher)
        return plain



class PiAsim:
    def GenAsim(n = 2048):
        priv = rsa.generate_private_key(
            public_exponent = 65537,
            key_size = n
        )
        pub = priv.public_key()
        return priv,pub

    def EncAsim(k , plain):
        cipher = k.encrypt(
            plain,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return cipher

    def DecAsim(k , cipher):
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
        digest = hashes.Hash(hashes.SHA256())
        digest.update(value)
        hash = digest.finalize()
        return digest

    def HVrfy(value, hash):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(value)
        newhash = digest.finalize()
        return newhash == hash

class S:
    def Sign(k, value):
        sign = k.sign(
            value,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return sign

    def Vrfy(k, value, sign):
        try:
            k.verify(
                sign,
                value,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False