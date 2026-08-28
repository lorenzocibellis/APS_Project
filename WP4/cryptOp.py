from cryptography.hazmat.primitives.asymmetric import rsa


class piSim:
    def genSim():
        return

    def encSim():
        return

    def decSim():
        return



class piAsim:
    def genAsim(n = 2048):
        priv = rsa.generate_private_key(
            public_exponent = 65537,
            key_size = n
        )
        pub = priv.public_key()
        return priv,pub

    def encAsim():
        return

    def decAsim():
        return


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