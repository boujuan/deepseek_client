# DeepSeek Model Chat Client with Voice Script - `deepseek-client`

This Python package provides a command-line interface to interact with the DeepSeek R1 language model. It supports text-based chat, voice output using Replicate's Kokoro TTS, customizable system prompts, and encrypted API key management for security.  This version is packaged as an installable Python package named `deepseek-r1-client` and is run using the `deepseek-client` command.

## Features

*   **Interactive Chat:** Engage in conversations with the DeepSeek R1 model directly from your terminal.
*   **Voice Output (TTS):** Hear the model's responses using voice synthesis via Replicate's Kokoro TTS API.
*   **System Prompts:** Customize the model's behavior with predefined system prompts or provide your own custom prompts.
*   **Configuration via YAML:** Manage settings like model selection, voice, and system prompts through a default `config.yaml` file included in the package.
*   **Command-Line Arguments:** Override `config.yaml` settings on the fly using command-line arguments.
*   **Encrypted API Keys:** Securely store your API keys using password-based encryption in `~/.deepseek/keys.enc`.
*   **Clean Output:** Beautifully formatted and colored terminal output for a pleasant user experience.
*   **Automatic Audio File Cleanup:** Automatically deletes old audio output files at the start of each session. Audio files are saved in `~/.deepseek/tts_output/`.

## Prerequisites

Before installing and running `deepseek-client`, ensure you have the following:

1.  **Python 3.11 or higher:**  Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

2.  **Required Python Packages:** These will be automatically installed when you install the `deepseek-r1-client` package, but for reference, they are:

    *   `openai`
    *   `replicate`
    *   `pyyaml`
    *   `cryptography`

3.  **API Keys:**
    *   **DeepSeek API Key:** Obtain an API key from [DeepSeek AI](https://api.deepseek.com/). You might need to create an account and find your API key in their dashboard.
    *   **Replicate API Token:** Get a Replicate API token from [Replicate](https://replicate.com/). Sign up or log in and find your API token in your account settings. (Required for voice output only).

## Installation Instructions

Follow these steps to install the `deepseek-r1-client` Python package:

1.  **Clone the Repository:** Clone this GitHub repository to your local machine if you haven't already. This step is necessary to install the package from the local directory.

    ```bash
    git clone https://github.com/boujuan/deepseek_client
    cd deepseek_client
    ```

2.  **Install the Python Package:** From the root directory of the cloned repository (where `setup.py` and `pyproject.toml` are located), install the package using pip:

    ```bash
    pip install .
    ```

    This command will install the `deepseek-r1-client` package into your Python environment, making the `deepseek-client` command available in your terminal.

## Setup Instructions (API Keys and Configuration)

After installing the package, you need to set up your API keys. The first time you run `deepseek-client`, it will guide you through creating and encrypting your API keys.

1.  **Run `deepseek-client` for the first time:**

    ```bash
    deepseek-client
    ```

    The first time you run `deepseek-client`, it will detect that API keys are not yet set up and will prompt you to:
    *   Enter your DeepSeek API Key.
    *   Enter your Replicate API Token (optional, only needed for voice output).
    *   Create and confirm an encryption password. This password will be used to protect your API keys.

    Upon providing the API keys and password, the script will:
    *   Create a `keys.yaml` file in `~/.deepseek/` containing your API keys (temporarily).
    *   Encrypt `keys.yaml` and save the encrypted keys to `~/.deepseek/keys.enc`.
    *   **Securely delete `keys.yaml`** after encryption.

    **Important:** Remember the encryption password you set. You will need it every time you run `deepseek-client` to decrypt your API keys.

## Running the Chat Client

To start chatting with the DeepSeek model, simply run the `deepseek-client` command from your terminal:

```bash
deepseek-client
```

You will be prompted to enter your decryption password. After successful decryption, you can start typing your prompts and interacting with the model.

### Command-Line Arguments (Override Configuration)

You can use command-line arguments to override the default settings from the `config.yaml` file and customize the behavior of `deepseek-client`:

*   **`-m <model_name>` or `--model <model_name>`**: Override the model specified in `config.yaml`. Choose between `deepseek-chat` or `deepseek-reasoner`.
    ```bash
    deepseek-client -m deepseek-chat
    ```

*   **`-v [voice_name]` or `--voice [voice_name]`**: Enable voice output. Optionally specify a voice name. If no voice name is provided, the default voice from `config.yaml` (`af_bella`) will be used. For voice options, see [Replicate Kokoro TTS documentation](https://replicate.com/jaaari/kokoro-82m).
    ```bash
    deepseek-client -v # Enable voice with default voice
    deepseek-client -v en_us_jesse # Enable voice and set voice to en_us_jesse
    ```

*   **`-p <prompt_name>` or `--prompt <prompt_name>`**: Select a system prompt from the `system_prompts` section in the default `config.yaml`. Available prompts are `default`, `developer`, and `brief`.
    ```bash
    deepseek-client -p developer # Use the 'developer' system prompt
    ```

*   **`-sp "<custom_prompt>"` or `--systemprompt "<custom_prompt>"`**: Provide a custom system prompt directly from the command line.
    ```bash
    deepseek-client -sp "You are a helpful and concise assistant."
    ```

**Example Usage with Arguments:**

```bash
deepseek-client -m deepseek-chat -v -p brief
```
This command will run the client using the `deepseek-chat` model, enable voice output with the default voice, and use the `brief` system prompt.

## File Structure After Installation

After installation, the core package files are located in your Python environment's site-packages directory. User-specific configuration and data are stored in the `~/.deepseek/` directory in your home directory:

```
~/.deepseek/                 (User's DeepSeek configuration directory)
├── keys.enc                (Encrypted API keys)
├── keys.yaml               (This file is created temporarily and deleted after encryption)
└── tts_output/             (Directory for audio output files)
    └── output_1.wav
    └── output_2.wav
    └── ...

<python_environment>/site-packages/deepseek/   (Package installation directory)
├── __init__.py
├── main.py                 (Main script - entry point for deepseek-client)
├── core/
│   ├── __init__.py
│   ├── auth.py
│   ├── chat.py
│   ├── config.py
│   └── tts.py
├── data/
│   └── config.yaml         (Default configuration file)
└── keys/
    ├── __init__.py
    └── encryptor.py
```

*   **`~/.deepseek/keys.enc`**:  Encrypted file storing your API keys.
*   **`~/.deepseek/tts_output/`**: Directory where audio output files (`output_*.wav`) are saved.
*   **`<python_environment>/site-packages/deepseek/data/config.yaml`**: Default configuration file included with the package. You can modify system prompts, default model, voice settings etc. by customizing this file directly in the package installation directory, or by overriding settings via command-line arguments.

## Customization

*   **System Prompts:**  Modify the default system prompts in `<python_environment>/site-packages/deepseek/data/config.yaml` or override them using the `-p` or `-sp` command-line arguments.
*   **Voice Settings:** Change the default voice in `<python_environment>/site-packages/deepseek/data/config.yaml` or override it using the `-v` argument. Explore the [Replicate Kokoro TTS documentation](https://replicate.com/jaaari/kokoro-82m) for available voices.
*   **Model Selection:** Choose between `deepseek-chat` or `deepseek-reasoner` by modifying the `model` setting in `<python_environment>/site-packages/deepseek/data/config.yaml` or using the `-m` argument.

## Security Note

*   **Your API keys are encrypted and stored locally in `~/.deepseek/keys.enc`.**  Ensure you keep your decryption password secure. If you lose it, you will not be able to access your API keys, and you may need to re-encrypt them.
*   **Treat your API keys as sensitive information and avoid sharing them publicly.**
*   While `keys.yaml` is created temporarily during the initial setup, it is deleted immediately after encryption to minimize the risk of exposing unencrypted keys.

Enjoy using `deepseek-client`!