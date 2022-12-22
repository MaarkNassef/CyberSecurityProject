from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def encrypt(passwordText: str):
        key = b'\xf0\xc4DnX\x05\x8f\xad\xc3j\x0b\x0c\xb6\xaf<z'
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        passwordText = bytes(passwordText,'utf-8')
        ciphertext,tag= cipher.encrypt_and_digest(passwordText)
        data = {}
        data['credit'] = ciphertext
        data['credit_tag'] = tag
        data['credit_nonce'] = nonce
        return data

def decrypt(passwordCipherText:bytes,tag:bytes,nonce):
        key = b'\xf0\xc4DnX\x05\x8f\xad\xc3j\x0b\x0c\xb6\xaf<z'      
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = cipher.decrypt_and_verify(passwordCipherText,tag)
        return data

