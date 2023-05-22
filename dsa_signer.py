from Crypto.PublicKey import DSA
from Crypto.Hash import SHA512

# Sign the contents of the message
def sign(message, key):
    hash = SHA512.new(message).hexdigest()

    signature = key.sign(hash, 5)
    

    signed_message = message + "," + str(signature[0]) + ',' +str(signature[1])

    return signed_message



# Verify the authenticity of the message
def verify(signature, key, message):
    hash = SHA512.new(message).hexdigest()
    if key.verify(hash, signature):
        print("Authentic")
    else:
        print("Incorrect")


message = "Baboons rule! xDDDD"
key = DSA.generate(1024)
message = sign(message, key)
contents = message.rsplit(',', 2)
verifying = verify((int(contents[1]), int(contents[2])), publickey, contents[0])