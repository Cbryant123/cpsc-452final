import symmetric_key_lib  

print("input something")  
tmp = input()  

# Convert string to bytes
tmp_bytes = tmp.encode()

ciphertext = symmetric_key_lib.aes_enc(tmp_bytes, b'asdfasdfasdfasdf')  
print(ciphertext)  

plaintext = symmetric_key_lib.aes_dec(ciphertext, b'asdfasdfasdfasdf')  

# Convert bytes back to string for printing
plaintext_str = plaintext.decode()
print(plaintext_str)
