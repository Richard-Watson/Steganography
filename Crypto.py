import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def crypt(bytestring, password, mode = True):
    password = bytes(password, encoding="UTF-8")
    salt = b'l,4B<\x0e\xff#\xc2\xe8\xe59\xbe\xdf8C'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)

    if mode:
        token = f.encrypt(bytestring)
        return token
    else:
        try:
            return f.decrypt(bytestring)
        except InvalidToken:
            print("Неверный ключ")