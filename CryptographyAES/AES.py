from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# encrypt credit card text by AES encryption
def encrypt(CreditText: str):
        #key with bytes
        key = b'\xf0\xc4DnX\x05\x8f\xad\xc3j\x0b\x0c\xb6\xaf<z'
        cipher = AES.new(key, AES.MODE_EAX)
        #generate random number
        nonce = cipher.nonce
        CreditText = bytes(CreditText,'utf-8')
        ciphertext,tag= cipher.encrypt_and_digest(CreditText)
        data = {}
        data['credit'] = ciphertext
        data['credit_tag'] = tag
        data['credit_nonce'] = nonce
        return data
# decrypt credit card text by AES encryption
def decrypt(CreditCipherText:bytes,tag:bytes,nonce):
        key = b'\xf0\xc4DnX\x05\x8f\xad\xc3j\x0b\x0c\xb6\xaf<z'      
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = cipher.decrypt_and_verify(CreditCipherText,tag)
        return data

