from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import getpass
import os
import base64
import yaml

class API_Encryptor:
    def __init__(self, secrets_yaml_path="keys/keys.yaml", secrets_enc_path="keys/keys.enc"):
        self.secrets_yaml_path = secrets_yaml_path
        self.secrets_enc_path = secrets_enc_path

    def _derive_key(self, password):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return salt, key

    def encrypt_secrets_file(self):
        password = getpass.getpass("Enter encryption password to create keys.enc: ").encode()
        salt, key = self._derive_key(password)
        cipher_suite = Fernet(key)

        try:
            with open(self.secrets_yaml_path, "rb") as f:
                plaintext = f.read()
        except FileNotFoundError:
            print(f"Error: {self.secrets_yaml_path} not found. Please create it first with your API keys.")
            return False

        encrypted = cipher_suite.encrypt(plaintext)

        with open(self.secrets_enc_path, "wb") as f:
            f.write(salt + encrypted)

        print(f"Encryption successful! {self.secrets_enc_path} created.")

        try:
            os.remove(self.secrets_yaml_path)
            print(f"Deleted {self.secrets_yaml_path} for security reasons.")
        except Exception as e:
            print(f"Warning: Failed to delete {self.secrets_yaml_path}. Please delete it manually for security. Error: {e}")

        return True

    def create_secrets_yaml_and_encrypt(self):
        print(f"Creating {self.secrets_yaml_path}...")
        deepseek_api_key = input("Enter your DeepSeek API Key: ")
        replicate_api_token = input("Enter your Replicate API Token: ")

        secrets_data = {
            "DEEPSEEK_API_KEY": deepseek_api_key,
            "REPLICATE_API_TOKEN": replicate_api_token,
        }

        with open(self.secrets_yaml_path, 'w') as yaml_file:
            yaml.dump(secrets_data, yaml_file)
        print(f"{self.secrets_yaml_path} created.")

        if self.encrypt_secrets_file():
            try:
                os.remove(self.secrets_yaml_path)
                print(f"Deleted {self.secrets_yaml_path} for security reasons.")
            except Exception as e:
                print(f"Warning: Failed to delete {self.secrets_yaml_path}. Please delete it manually for security. Error: {e}")
            return True
        else:
            return False


if __name__ == "__main__":
    encryptor = API_Encryptor()