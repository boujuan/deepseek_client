import yaml
import argparse

class ConfigManager:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.config = self._load_base_config()
        
    def _load_base_config(self):
        with open(self.config_path) as f:
            return yaml.safe_load(f)
    
    def apply_cli_args(self, args):
        if args.model:
            self.config['model'] = args.model
        if args.prompt:
            self.config['selected_prompt'] = args.prompt
            self.config['custom_system_prompt'] = None
        if args.systemprompt:
            self.config['custom_system_prompt'] = args.systemprompt
            self.config['selected_prompt'] = None
        if args.voice is not None:
            self.config['use_voice'] = True
            self.config['voice'] = args.voice if isinstance(args.voice, str) else "af_bella"
    
    @staticmethod
    def create_parser():
        parser = argparse.ArgumentParser(description="DeepSeek R1 Chat")
        parser.add_argument('-m', '--model', help='Override model from config')
        parser.add_argument('-v', '--voice', nargs='?', const=True, 
                          help='Enable voice output with optional voice name')
        parser.add_argument('-p', '--prompt', help='Select system prompt')
        parser.add_argument('-sp', '--systemprompt', help='Set custom system prompt')
        return parser 