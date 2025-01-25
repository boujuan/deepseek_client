from core.auth import SecretManager
from core.config import ConfigManager
from core.chat import ChatClient
from core.tts import TTSService
import sys
import os

# Color codes for console output
RED = '\033[91m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

class ChatApplication:
    def __init__(self):
        self.secrets = SecretManager().load_secrets()
        self.config_mgr = ConfigManager()
        self.args = self._parse_arguments()
        self._apply_configuration()
        self.chat_client = ChatClient(self.secrets['DEEPSEEK_API_KEY'])
        self.tts_service = TTSService() if self.config_mgr.config['use_voice'] else None

    def _parse_arguments(self):
        parser = ConfigManager.create_parser()
        return parser.parse_args()

    def _apply_configuration(self):
        self.config_mgr.apply_cli_args(self.args)
        self.config = self.config_mgr.config
        self._validate_voice_config()

    def _validate_voice_config(self):
        if self.config['use_voice'] and 'REPLICATE_API_TOKEN' not in self.secrets:
            print(f"{RED}⚠️ Voice requires REPLICATE_API_TOKEN in secrets{RESET_COLOR}")
            sys.exit(1)
        if self.config['use_voice']:
            os.environ["REPLICATE_API_TOKEN"] = self.secrets['REPLICATE_API_TOKEN']

    def _get_prompt_prefixes(self):
        model_name = self.config['model'].upper()
        prefix_length = 8 + len(model_name)
        return {
            'user': f"{RED}👤 YOU [{{}}]<{{}}{RESET_COLOR}> ",
            'bot': f"{BLUE}🤖 {model_name} [{{}}]<{{}}{RESET_COLOR}> ",
            'length': prefix_length
        }

    def run(self):
        print(f"{PURPLE}👋 Welcome to DeepSeek R1 Model 🤖{RESET_COLOR}")
        prefixes = self._get_prompt_prefixes()
        prompt_number = 0

        while True:
            prompt_number += 1
            user_input = self._get_user_input(prompt_number, prefixes)
            if user_input.lower() in {'exit', 'end', 'quit'}:
                break
            
            response = self.chat_client.get_response(user_input, self.config)
            self._show_response(response, prompt_number, prefixes)
            
            if self.tts_service:
                self.tts_service.synthesize(response, prompt_number, self.config['voice'])

    def _get_user_input(self, prompt_number, prefixes):
        user_prompt = prefixes['user'].format(prompt_number, ' ' * prefixes['length'])
        return input(user_prompt).strip()

    def _show_response(self, response, prompt_number, prefixes):
        bot_prompt = prefixes['bot'].format(prompt_number, ' ' * prefixes['length'])
        print(f"{bot_prompt}{response}")

if __name__ == "__main__":
    try:
        app = ChatApplication()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{RED}🚪 Exiting...{RESET_COLOR}")
        sys.exit(0)
    except Exception as e:
        print(f"{RED}⚠️ Critical error: {e}{RESET_COLOR}")
        sys.exit(1) 