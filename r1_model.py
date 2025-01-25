import argparse
from openai import OpenAI
import replicate
import subprocess
import os
import yaml
import getpass
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import glob
from keys.encryptor import API_Encryptor

RED = '\033[91m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

# Load keys.yaml API keys for deepseek and replicate
def load_secrets():
    secrets_enc_path = "keys/keys.enc"
    secrets_yaml_path = "keys/keys.yaml"

    if not os.path.exists(secrets_enc_path): # Check if keys.enc exists
        print(f"{RED}keys.enc not found.{RESET_COLOR}")
        if os.path.exists(secrets_yaml_path): # Check if keys.yaml exists
            print(f"{GREEN}Encrypting keys.yaml to create keys.enc...{RESET_COLOR}")
            encryptor = API_Encryptor()
            if not encryptor.encrypt_secrets_file(): # Encrypt keys.yaml
                print(f"{RED}Encryption failed. Please check {secrets_yaml_path} and try again.{RESET_COLOR}")
                return None
        else: # If keys.yaml also doesn't exist
            print(f"{GREEN}keys.yaml not found. Creating it and encrypting to keys.enc...{RESET_COLOR}")
            encryptor = API_Encryptor()
            if not encryptor.create_secrets_yaml_and_encrypt(): # Create keys.yaml and encrypt
                print(f"{RED}Failed to create and encrypt keys. Please check and try again.{RESET_COLOR}")
                return None


    while True:
        password = getpass.getpass(f"{GREEN}Enter decryption password: {RESET_COLOR}").encode()
        print()
        try:
            with open(secrets_enc_path, "rb") as f:
                data = f.read()
                salt = data[:16]
                encrypted_data = data[16:]

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=480000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))

            cipher_suite = Fernet(key)
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            return yaml.safe_load(decrypted_data)

        except InvalidToken:
            print(f"{RED}⚠️ Decryption failed: Incorrect password. Please try again.{RESET_COLOR}")
            continue
        except Exception as e:
            print(f"{RED}⚠️ Error loading keys: {e}{RESET_COLOR}")
            return None

# Load config.yaml and client for deepseek with API key
def load_config(args):
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    secrets = load_secrets()
    if secrets is None: # Exit if secrets loading failed in load_secrets()
        print(f"{RED}Failed to load keys. Exiting.{RESET_COLOR}")
        exit(1)

    client = OpenAI(api_key=secrets['DEEPSEEK_API_KEY'], base_url="https://api.deepseek.com")
    os.environ["REPLICATE_API_TOKEN"] = secrets['REPLICATE_API_TOKEN']

    if args.model:
        config['model'] = args.model
    if args.prompt:
        config['selected_prompt'] = args.prompt
        config['custom_system_prompt'] = None
    if args.systemprompt:
        config['custom_system_prompt'] = args.systemprompt
        config['selected_prompt'] = None
    if args.voice is not None:
        config['use_voice'] = True
        if isinstance(args.voice, str):
            config['voice'] = args.voice
        elif args.voice is True and 'voice' not in config:
            config['voice'] = "af_bella"

    return config, client

# Function to chat with the model
def chat(user_input, config):
    system_prompt_content = ""
    if config.get('custom_system_prompt'):
        system_prompt_content = config['custom_system_prompt']
    elif config.get('selected_prompt'):
        system_prompt_content = config['system_prompts'][config['selected_prompt']]
    else:
        system_prompt_content = config['system_prompts']['default']

    messages=[
        {"role": "system", "content": system_prompt_content},
        {"role": "user", "content": user_input},
    ]
    response = client.chat.completions.create(
        model=config['model'],
        messages=messages,
        stream=False
    )
    answer = response.choices[0].message.content
    return answer

# Function to say the answer via Kokoro TTS API in replicate
def say(text, prompt_number, config):
    input = {
        "text": text,
        "voice": config['voice'],
        "speed": 1.1, # 0.1 - 1.5
    }
    output = replicate.run(
        "jaaari/kokoro-82m:dfdf537ba482b029e0a761699e6f55e9162cfd159270bfe0e44857caa5f275a6",
        input=input,
    )
    output_filename = f"output/output_{prompt_number}.wav"
    with open(output_filename, "wb") as f:
        f.write(output.read())

    subprocess.run([
        'ffplay',
        '-autoexit',
        '-nodisp',
        '-loglevel', 'quiet',
        output_filename
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    print(f"{PURPLE}👋 Welcome to DeepSeek R1 Model 🤖{RESET_COLOR}")

    output_files = glob.glob('output/output_*.wav')
    for file_path in output_files:
        try:
            os.remove(file_path)
            # print(f"{GREEN}🗑️ Deleted old output file: {file_path}{RESET_COLOR}")
        except Exception as e:
            print(f"{RED}⚠️ Error deleting {file_path}: {e}{RESET_COLOR}")

    # Argument parsing
    parser = argparse.ArgumentParser(description="DeepSeek R1 Model Chat Script")
    parser.add_argument('-m', '--model', type=str, help='Override model name from config.yaml')
    parser.add_argument('-v', '--voice', nargs='?', const=True, default=None,
                        help='Enable voice output. Optionally specify voice name after -v (e.g., -v af_bella)')
    parser.add_argument('-p', '--prompt', type=str, help='Select system prompt from config.yaml')
    parser.add_argument('--systemprompt', '-sp', type=str, help='Set a custom system prompt directly')
    args = parser.parse_args()

    config, client = load_config(args)

    model_name = config['model'].upper()
    model_name_length = len(model_name)
    prefix_width = 8 + model_name_length

    prompt_number = 0
    while True:
        prompt_number += 1
        you_prompt_prefix = f"👤 YOU [{prompt_number}]"
        formatted_you_prompt = f"{RED}{you_prompt_prefix:<{prefix_width}}{RESET_COLOR}> "
        user_input = input(formatted_you_prompt)
        if user_input == "exit" or user_input == "end" or user_input == "quit":
            break

        answer = chat(user_input, config) # Pass 'config' to chat
        deepseek_prompt_prefix = f"🤖 {model_name} [{prompt_number}]"
        formatted_deepseek_prompt = f"{BLUE}{deepseek_prompt_prefix:<{prefix_width}}{RESET_COLOR}> "
        print(formatted_deepseek_prompt + answer)

        if config['use_voice']:
            say(answer, prompt_number, config)
