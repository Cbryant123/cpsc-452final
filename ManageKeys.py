from Crypto import Random
from Crypto.PublicKey import DSA
from Crypto.PublicKey import RSA
import Crypto.PublicKey.DSA as DSA
import Crypto.PublicKey.RSA as RSA
import base64

# Generate a pair of private and public keys
def GenerateKeys():
	# 256 and >= 1024
	modSize = 256*4

	privateKey = RSA.generate(modSize, Random.new().read)
	publicKey = privateKey.publickey()
	return privateKey, publicKey


def PublicEncryption(message, publicKey):
	encryptMessage = publicKey.encrypt(message, 32)[0]
	encMessage = base64.b64encode(encryptMessage)
	return encMessage


def PrivateDecryption(encMessage, privateKey):
	decodeAnalyticMessage = base64.b64decode(encMessage)
	decryptedMessage = privateKey.decrypt(decodeAnalyticMessage)
	return decryptedMessage

def GeneratesDigitalSignature(symmetricKey, privateKey, alg):
    hash = MD5.new(symmetricKey).digest()
    print((repr(hash)))

    K = ''
    if alg == RSA:
        K = CUN.getRandomNumber(16, os.urandom)
    elif alg == DSA:
        K = CUN.getRandomNumber(16, os.urandom)

    signature = privateKey.sign(hash, K)

    return signature
