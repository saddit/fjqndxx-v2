from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT


def decrypt(src: str, key: str) -> str:
    crypt_sm4 = CryptSM4()
    secret_key = bytes.fromhex(key)
    # print(secret_key)
    crypt_sm4.set_key(secret_key, SM4_DECRYPT)
    # 将转入参数base64.b64decode解码成十六进制的bytes类型
    byt_cipher_text = bytes.fromhex(src)
    # 调用加密方法解密，解密后为bytes类型
    decrypt_value = crypt_sm4.crypt_ecb(byt_cipher_text)

    return decrypt_value.decode()


def encrypt(src: str, key: str) -> str:
    # 创建 SM4对象
    crypt_sm4 = CryptSM4()
    # 定义key值
    secret_key = bytes.fromhex(key)

    # 设置key
    crypt_sm4.set_key(secret_key, SM4_ENCRYPT)

    # 调用加密方法加密(十六进制的bytes类型)
    encrypt_value = crypt_sm4.crypt_ecb(src.encode(encoding="utf-8"))

    # 返回加密后的字符串
    return encrypt_value.hex()


if __name__ == '__main__':
    s_key = "A7E74D2B6282AEB1C5EA3C28D25660A7"
    plain_text = '15106014293'
    res = encrypt(plain_text, s_key)
    print(res)

    cipher_text = '635EA5ABD3C425EB7A80D223C2BA6305'
    res = decrypt(cipher_text, s_key)
    print(res)
