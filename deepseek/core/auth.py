from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import os
from pathlib import Path
import yaml
import getpass
from deepseek.keys.encryptor import API_Encryptor

class SecretManager:
    def __init__(self, enc_path=None, yaml_path=None):
        deepseek_dir = Path.home() / ".deepseek"
        os.makedirs(deepseek_dir, exist_ok=True)

        if not enc_path:
            enc_path = str(deepseek_dir / "keys.enc")
        if not yaml_path:
            yaml_path = str(deepseek_dir / "keys.yaml")

        self.enc_path = enc_path
        self.yaml_path = yaml_path
        
    def load_secrets(self):
        if not os.path.exists(self.enc_path):
            self._handle_missing_enc_file()
        return self._decrypt_secrets()

    def _handle_missing_enc_file(self):
        encryptor = API_Encryptor(self.yaml_path, self.enc_path)
        if os.path.exists(self.yaml_path):
            print("Encrypting existing keys.yaml...")
            if not encryptor.encrypt_secrets_file():
                raise RuntimeError("Encryption failed")
        else:
            print("Creating new keys.yaml...")
            if not encryptor.create_secrets_yaml_and_encrypt():
                raise RuntimeError("Key creation failed")

    def _decrypt_secrets(self):
        while True:
            try:
                password = getpass.getpass("Enter decryption password: ").encode()
                with open(self.enc_path, "rb") as f:
                    data = f.read()
                    salt, encrypted_data = data[:16], data[16:]
                
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=480000,
                )
                key = base64.urlsafe_b64encode(kdf.derive(password))
                return yaml.safe_load(Fernet(key).decrypt(encrypted_data))
                
            except InvalidToken:
                print("⚠️ Incorrect password, try again")
            except Exception as e:
                raise RuntimeError(f"Decryption error: {e}") 