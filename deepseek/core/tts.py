import replicate
import subprocess
import os
import glob

class TTSService:
    def __init__(self):
        self.output_dir = "output"
        self._clean_old_files()
        
    def synthesize(self, text, prompt_number, voice="af_bella", speed=1.1):
        output = replicate.run(
            "jaaari/kokoro-82m:dfdf537ba482b029e0a761699e6f55e9162cfd159270bfe0e44857caa5f275a6",
            input={"text": text, "voice": voice, "speed": speed}
        )
        self._save_and_play(output, prompt_number)
    
    def _save_and_play(self, output, prompt_number):
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, f"output_{prompt_number}.wav")
        
        with open(output_path, "wb") as f:
            f.write(output.read())
            
        subprocess.run([
            'ffplay', '-autoexit', '-nodisp', '-loglevel', 'quiet', output_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    def _clean_old_files(self):
        for file in glob.glob(os.path.join(self.output_dir, 'output_*.wav')):
            try: os.remove(file)
            except: pass 