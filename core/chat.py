from openai import OpenAI

class ChatClient:
    def __init__(self, api_key, base_url="https://api.deepseek.com"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        
    def get_response(self, user_input, config):
        system_prompt = self._get_system_prompt(config)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        response = self.client.chat.completions.create(
            model=config['model'],
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content
    
    def _get_system_prompt(self, config):
        if config.get('custom_system_prompt'):
            return config['custom_system_prompt']
        if config.get('selected_prompt'):
            return config['system_prompts'][config['selected_prompt']]
        return config['system_prompts']['default'] 