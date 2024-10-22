from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
import os
import base64

"""
# requirement 
# - python 3.11
# - dotenv
# - cryptography


# .env 
# API_KEY = your api key

# 사용 예제)

private_key = CipherKey()
enc = Encrypt(private_key) 
enc.encryption() # Applied encryption to the API key.(Execute only once at the beginning)

# .env (after encrypted)
# API_KEY = Your encrypted API key

# Decrypt는 translator.py 참고
"""


# openAI api key 암호화/복호화
class CipherKey:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CipherKey, cls).__new__(cls)
            cls._instance._load_key()
        return cls._instance

    def _load_key(self):
        if os.path.exists(".pem"):
            with open(".pem", "rb") as key_file:
                pem = key_file.read()
                self.key, self.nonce = self._from_pem(pem)
        else:
            self.key = os.urandom(32)
            self.nonce = os.urandom(16)
            self._save_pem(self.key, self.nonce)

    def _save_pem(self, key, nonce):
        private_key = key + nonce
        pem = self._to_pem(private_key)
        with open(".pem", "wb") as key_file:
            key_file.write(pem.encode("utf-8"))

    def _to_pem(self, key):
        private_key_to_pem = base64.b64encode(key).decode("utf-8")
        pem = "-----BEGIN KEY-----\n"
        for i in range(0, len(private_key_to_pem), 64):
            pem += private_key_to_pem[i : i + 64] + "\n"
        pem += "-----END KEY-----\n"
        return pem

    def _from_pem(self, pem):
        line_by_pem = pem.decode("utf-8").splitlines()
        pem_to_private_key = "".join(line_by_pem[1:-1])
        private_key = base64.b64decode(pem_to_private_key)
        key = private_key[:32]
        nonce = private_key[32:]
        return key, nonce


class Encrypt:
    def __init__(self, cipher_key):
        self._cipher_key = cipher_key

    def encryption(self):
        plain = os.environ.get("API_KEY").encode("utf-8")
        cipher = Cipher(
            algorithms.ChaCha20(self._cipher_key.key, self._cipher_key.nonce), mode=None
        )
        encryptor = cipher.encryptor()
        cipher_text = encryptor.update(plain) + encryptor.finalize()
        to_base64 = f"API_KEY = {base64.b64encode(cipher_text + self._cipher_key.nonce).decode('utf-8')}"
        with open(".env", "wb") as file:
            file.write(to_base64.encode("utf-8"))


class Decrypt:
    def __init__(self, cipher_key):
        self._cipher_key = cipher_key

    def decryption(self):
        with open(".env", "rb") as file:
            crypto = file.read().decode("utf-8")
            base64_api_key = crypto.split("API_KEY = ")[-1]
            api_key = base64.b64decode(base64_api_key)
            nonce = api_key[-16:]
            cipher_text = api_key[:-16]
            cipher = Cipher(
                algorithms.ChaCha20(self._cipher_key.key, nonce),
                mode=None,
            )
            decryptor = cipher.decryptor()
            plain_text = decryptor.update(cipher_text).decode("utf-8")
            return plain_text
