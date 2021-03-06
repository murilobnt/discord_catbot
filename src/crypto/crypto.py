from Crypto.Cipher import AES
import base64
import os

def encrypt_val(clear_text):
    enc_secret = AES.new(os.environ['CRYPTO_MASTER_KEY'][:32])
    tag_string = (str(clear_text) +
                  (AES.block_size -
                   len(str(clear_text)) % AES.block_size) * "\0")
    cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))

    return str(cipher_text.decode("utf-8"))

def decrypt_val(cipher_text):
    dec_secret = AES.new(os.environ['CRYPTO_MASTER_KEY'][:32])
    raw_decrypted = dec_secret.decrypt(base64.b64decode(cipher_text))
    clear_val = raw_decrypted.decode().rstrip("\0")
    return clear_val
