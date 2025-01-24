from openai import OpenAI
import replicate
import subprocess
import os

client = OpenAI(api_key="sk-c556575f27ff4aefa1133e54e3d4949e", base_url="https://api.deepseek.com")
os.environ["REPLICATE_API_TOKEN"] = "r8_BJuI4iVLB7oCT2tMTDweg2AoA6cIYnz0q5JDs"

#################### CONFIG ####################
SYSTEM_PROMPT = "You are a helpful assistant"
MODEL = "deepseek-reasoner"
USE_VOICE = False
VOICE = "af_bella" # "af", "af_bella", "af_sarah", "am_adam", "am_michael", "bf_emma", "bf_isabella", "bm_george", "bm_lewis", "af_nicole", "af_sky"
#################################################

# Function to chat with the model
def chat(user_input):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        stream=False
    )
    answer = response.choices[0].message.content
    return answer

# Function to say the answer via Kokoro TTS API in replicate
def say(text):
    input = {
        "text": text,
        "voice": VOICE,
        "speed": 1.1, # 0.1 - 1.5
    }
    output = replicate.run(
        "jaaari/kokoro-82m:dfdf537ba482b029e0a761699e6f55e9162cfd159270bfe0e44857caa5f275a6",
        input=input,
    )
    with open("output.wav", "wb") as f:
        f.write(output.read())
    
    subprocess.run([
        'ffplay',
        '-autoexit',
        '-nodisp',
        '-loglevel', 'quiet',
        'output.wav'
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    print("Welcome to DeepSeek R1 Model")
    while True:
        user_input = input("YOU > ")
        if user_input == "exit" or user_input == "end" or user_input == "quit":
            break
        answer = chat(user_input)
        print("DEEPSEEK > ", answer)
        
        if USE_VOICE:
            say(answer)
