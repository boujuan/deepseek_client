# DeepSeek Model Chat Client with Voice Script

This Python script provides a command-line interface to interact with the DeepSeek R1 language model. It supports text-based chat, voice output using Replicate's Kokoro TTS, customizable system prompts, and encrypted API key management for security.

## Features

*   **Interactive Chat:** Engage in conversations with the DeepSeek R1 model directly from your terminal.
*   **Voice Output (TTS):** Hear the model's responses using voice synthesis via Replicate's Kokoro TTS API.
*   **System Prompts:** Customize the model's behavior with predefined system prompts or provide your own custom prompts.
*   **Configuration via YAML:** Manage settings like model selection, voice, and system prompts through a `config.yaml` file.
*   **Command-Line Arguments:** Override `config.yaml` settings on the fly using command-line arguments.
*   **Encrypted API Keys:** Securely store your API keys using password-based encryption.
*   **Clean Output:** Beautifully formatted and colored terminal output for a pleasant user experience.
*   **Automatic Audio File Cleanup:** Automatically deletes old audio output files at the start of each session.

## Prerequisites

Before running the script, ensure you have the following:

1.  **Python 3.11 or higher:**  Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

2.  **Required Python Packages:** Install the necessary Python libraries using pip/conda/mamba:

    ```bash
    pip install openai replicate pyyaml cryptography
    ```

    ```bash
    conda install openai replicate pyyaml cryptography
    ```

    ```bash
    mamba install openai replicate pyyaml cryptography
    ```

3.  **API Keys:**
    *   **DeepSeek API Key:** Obtain an API key from [DeepSeek AI](https://api.deepseek.com/). You might need to create an account and find your API key in their dashboard.
    *   **Replicate API Token:** Get a Replicate API token from [Replicate](https://replicate.com/). Sign up or log in and find your API token in your account settings.

## Setup Instructions

Follow these steps to set up and run the script:

1.  **Clone the Repository:** Clone this GitHub repository to your local machine.
   
    ```bash
    git clone https://github.com/boujuan/deepseek
    ```

2.  **Create `secrets.yaml`:**  Inside the `keys/` directory, create a file named `secrets.yaml` and add your API keys as follows:

    ```yaml:keys/secrets.yaml
    DEEPSEEK_API_KEY: "YOUR_DEEPSEEK_API_KEY"
    REPLICATE_API_TOKEN: "YOUR_REPLICATE_API_TOKEN"
    ```
    **Replace `"YOUR_DEEPSEEK_API_KEY"` and `"YOUR_REPLICATE_API_TOKEN"` with your actual API keys.**

3.  **Encrypt `secrets.yaml`:** Run the `encrypt_secrets.py` script located in the `keys/` directory to encrypt your API keys.

    ```bash
    python keys/encrypt_secrets.py
    ```
    You will be prompted to enter and confirm an encryption password. **Remember this password!** It will be required to run the main script.

    This script will:
    *   Prompt you for an encryption password.
    *   Generate an encrypted file `secrets.enc` in the `keys/` directory.
    *   **It is crucial to delete the `secrets.yaml` file after encryption for security.**


4.  **Configure `config.yaml` (Optional):**  The `config.yaml` file in the root directory allows you to customize the script's behavior:

    ```yaml:config.yaml
    system_prompts:
      default: "You are a helpful assistant"
      developer: "You are a senior Python developer assisting with coding questions"
      brief: "You are a helpful assistant that provides very brief and concise answers"

    selected_prompt: "default" # Choose from system_prompts or use 'default'
    model: "deepseek-reasoner" # Choose between "deepseek-chat" or "deepseek-reasoner"
    use_voice: false # Set to true to enable voice output
    voice: "af_bella" # Voice for TTS (e.g., "af_bella", "en_us_jesse"). See Replicate Kokoro TTS documentation for options.
    ```

    *   **`system_prompts`**: Define system prompts that guide the model's responses.
    *   **`selected_prompt`**: Choose a default system prompt from `system_prompts` to use.
    *   **`model`**: Select the DeepSeek model to use (`deepseek-chat` or `deepseek-reasoner`).
    *   **`use_voice`**: Enable or disable voice output (TTS).
    *   **`voice`**:  Specify the voice for TTS (if `use_voice` is true). Look in the API from Kokoro for different voice options.

## Running the Script

To start chatting with the DeepSeek model, run the `r1_model.py` script from your terminal:

```bash
python r1_model.py
```

You will be prompted to enter your decryption password. After successful decryption, you can start typing your prompts and interacting with the model.

### Command-Line Arguments (Override `config.yaml`)

You can use command-line arguments to override the settings in `config.yaml` for more flexibility:

*   **`-r` or `--model <model_name>`**: Override the model specified in `config.yaml`.
    ```bash
    python r1_model.py -r deepseek-chat
    ```

*   **`-v` or `--voice [voice_name]`**: Enable voice output. Optionally specify a voice name. If no voice name is provided, the default voice from `config.yaml` or `af_bella` will be used.
    ```bash
    python r1_model.py -v # Enable voice with default voice
    python r1_model.py -v en_us_jesse # Enable voice and set voice to en_us_jesse
    ```

*   **`-p` or `--prompt <prompt_name>`**: Select a system prompt from the `system_prompts` section in `config.yaml`.
    ```bash
    python r1_model.py -p developer # Use the 'developer' system prompt
    ```

*   **`-sp` or `--systemprompt "<custom_prompt>"`**: Provide a custom system prompt directly from the command line.
    ```bash
    python r1_model.py -sp "You are a helpful and concise assistant."
    ```

**Example Usage with Arguments:**

```bash
python r1_model.py -r deepseek-chat -v -p brief
```
This command will run the script using the `deepseek-chat` model, enable voice output with the default voice, and use the `brief` system prompt.

## File Structure

```
deepseek-r1-chat/             (Root directory)
├── config.yaml               (Configuration file)
├── r1_model.py              (Main script to run the chat model)
├── keys/                     (Directory for key management)
│   ├── secrets.yaml        (File containing API keys)
│   ├── encrypt_secrets.py  (Script to encrypt secrets.yaml)
│   ├── secrets.enc         (Created after running encrypt_secrets.py)
├── output/                 (Directory for audio output files)
├── README.md               (This README file)
└── .gitignore              (Git ignore file)
```

*   **`config.yaml`**: Contains configuration settings for the script (model, prompts, voice, colors).
*   **`r1_model.py`**: The main Python script that runs the chat interface.
*   **`encrypt_secrets.py`**: Python script to encrypt the `secrets.yaml` file.
*   **`keys/secrets.enc`**:  Encrypted file storing API keys. **Do not commit `secrets.yaml`!**
*   **`output/`**: Directory where audio output files (`output_*.wav`) are saved.
*   **`README.md`**:  Documentation for the project.

## Customization

*   **System Prompts:**  Modify or add new system prompts in the `system_prompts` section of `config.yaml`.
*   **Voice Settings:** Change the default voice in `config.yaml` or override it using the `-v` argument. Explore the [Replicate Kokoro TTS documentation](https://replicate.com/jaaari/kokoro-82m) for available voices.

## Security Note

*   **Never commit `secrets.yaml` to version control.** Ensure it is added to your `.gitignore` file.
*   Keep your encryption password secure. If you lose it, you will not be able to decrypt your API keys.
*   Treat your API keys as sensitive information and avoid sharing them publicly.