import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


def encrypt(src, public_key):
    public_key = '-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----'
    rsa_key = RSA.importKey(public_key)
    cipher = PKCS1_v1_5.new(rsa_key)
    return str(base64.b64encode(cipher.encrypt(src.encode('utf-8'))), 'utf-8')