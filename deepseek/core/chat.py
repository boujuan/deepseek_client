from openai import OpenAI

class ChatClient:
    def __init__(self, api_key, base_url="https://api.deepseek.com"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.history = ChatHistory()
        
    def get_response(self, user_input, config):
        system_prompt = self._get_system_prompt(config)
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.history.get_messages())
        messages.append({"role": "user", "content": user_input})
        response = self.client.chat.completions.create(
            model=config['model'],
            messages=messages,
            stream=False
        )
        assistant_reply = response.choices[0].message.content
        self.history.add_message("user", user_input)
        self.history.add_message("assistant", assistant_reply)
        return assistant_reply
    
    def _get_system_prompt(self, config):
        if config.get('custom_system_prompt'):
            return config['custom_system_prompt']
        if config.get('selected_prompt'):
            return config['system_prompts'][config['selected_prompt']]
        return config['system_prompts']['default']
    
class ChatHistory:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []