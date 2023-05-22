import os, random, struct
import sys
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from base64 import b64encode, b64decode

##################################################
# Loads the RSA key object from the location
# @param keyPath - the path of the key
# @return - the RSA key object with the loaded key
##################################################
def loadKey(keyPath):

	# The RSA key
	key = None

	# Open the key file
	with open(keyPath, 'r') as keyFile:

		# Read the key file
		keyFileContent = keyFile.read()

		# Decode the key
		decodedKey = b64decode(keyFileContent)

		# Load the key
		key = RSA.importKey(decodedKey)

	# Return the key
	return key


##################################################
# Signs the string using an RSA private key
# @param sigKey - the signature key
# @param string - the string
##################################################
def digSig(sigKey, string):

	return sigKey.sign(string, '')

##########################################################
# Returns the file signature
# @param fileName - the name of the file
# @param privKey - the private key to sign the file with
# @return fileSig - the file signature
##########################################################
def getFileSig(message, privKey):

	#1 compute the hash of message
	hash = SHA512.new(message).hexdigest()
	#2 sign the message with the hash
	signed_hash = digSig(privKey, hash)
	# 4. Return the signed hash; this is your digital signature
	return signed_hash

###########################################################
# Verifies the signature of the file
# @param fileName - the name of the file
# @param pubKey - the public key to use for verification
# @param signature - the signature of the file to verify
##########################################################
def verifyFileSig(message, pubKey, signature):

	
	# 1. Compute the SHA-512 hash of the contents
	hash = SHA512.new(message).hexdigest()
	# 2. Use the verifySig function you implemented in
	# order to verify the file signature
	verify_sig = verifySig(hash, signature, pubKey)
	# 3. Return the result of the verification i.e.,
	# True if matches and False if it does not match
	return verify_sig


############################################
# Saves the digital signature to a file
# @param fileName - the name of the file
# @param signature - the signature to save
############################################
def saveSig(fileName, signature):

	# Signature is a tuple with a single value.
	# Get the first value of the tuple, convert it
	# to a string, and save it to the file (i.e., indicated
	# by fileName)
	first_value = str(signature[0])
	file = open(fileName, 'w')
	file.write(first_value)
	file.close()

###########################################
# Loads the signature and converts it into
# a tuple
# @param fileName - the file containing the
# signature
# @return - the signature
###########################################
def loadSig(message):

	# Load the signature from the specified file.
	# Open the file, read the signature string, convert it
	# into an integer, and then put the integer into a single
	# element tuple
	contents=message.rsplit(',',1)
	signature = (int(contents[1]), )
	return (contents[0], signature)

#################################################
# Verifies the signature
# @param theHash - the hash
# @param sig - the signature to check against
# @param veriKey - the verification key
# @return - True if the signature matched and
# false otherwise
#################################################
def verifySig(theHash, sig, veriKey):
	
	
	
	# Verify the hash against the provided
	# signature using the verify() function of the
	# key and return the result
	return veriKey.verify(theHash, sig)


def test(pubKeyPath, privKeyPath):
    message="I like to eat food everday all day"
    #set the public and private keys
    privateKey=loadKey(privKeyPath)
    publicKey=loadKey(pubKeyPath)
    #get the signature for message
    file_signature=getFileSig(message, privateKey)
    #append the signature to the end of message seperated by a comma
    message=message +','+str(file_signature[0])
    #loadsig seperates the message and signature 
    (message, file_signature)=loadSig(message)

    #verify the signature
    if verifyFileSig(message,publicKey, file_signature):
        print("signature matches")
    else:
        print("you screwed up")

# if len(sys.argv)>2:
# 	test(sys.argv[1], sys.argv[2])
# else:
# 	print("missing arguments")