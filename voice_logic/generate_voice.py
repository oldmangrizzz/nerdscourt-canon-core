
import os
from dotenv import load_dotenv
import requests

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

def generate_agent_voice(text_input, audio_prompt_url=None):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    payload = {
        "text_input": text_input,
        "audio_prompt_input": audio_prompt_url,
        "max_new_tokens": 3072,
        "cfg_scale": 3.0,
        "temperature": 1.3,
        "top_p": 0.95,
        "cfg_filter_top_k": 30,
        "speed_factor": 0.94
    }

    response = requests.post(
        "https://hf.space/embed/nari-labs/Dia-1.6B/+/api/predict",
        headers=headers,
        json={"data": list(payload.values())}
    )

    if response.ok:
        result = response.json()
        return result.get("data", [None])[0]
    else:
        print("Error:", response.status_code, response.text)
        return None
