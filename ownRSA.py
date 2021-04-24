from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def pub_encrypt(plaintext, cert):
    pubkey = RSA.import_key(cert)
    cipher = PKCS1_OAEP.new(pubkey)    
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

def priv_decrypt(ciphertext, server_key_path, passphrase):
    try:
        with open(server_key_path, "rb") as server_key_file:
            server_key_data = server_key_file.read()
            privkey = RSA.importKey(server_key_data, passphrase=passphrase)
            cipher = PKCS1_OAEP.new(privkey)
            plaintext = cipher.decrypt(ciphertext)
            return plaintext
    except FileNotFoundError as e:
        print(e)
        return False

