from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import getpass
import os
import base64

# Generate key from password
password = getpass.getpass("Enter encryption password: ").encode()
salt = os.urandom(16)

# Derive Fernet key using PBKDF2
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))

cipher_suite = Fernet(key)
with open("keys/secrets.yaml") as f:
    plaintext = f.read().encode()

encrypted = cipher_suite.encrypt(plaintext)

with open("keys/secrets.enc", "wb") as f:
    f.write(salt + encrypted)

print("Encryption successful! secrets.enc created.") 