
import os
import requests
from dotenv import load_dotenv

load_dotenv()

CONVEX_URL = os.getenv("CONVEX_DEPLOYMENT_URL")

def push_persona_to_convex(persona):
    url = f"{CONVEX_URL}/functions/spawnPersona"
    response = requests.post(url, json=persona)
    if response.ok:
        return response.json()
    else:
        print("Error pushing persona:", response.status_code, response.text)
        return None

def push_trial_to_convex(trial):
    url = f"{CONVEX_URL}/functions/generateTrial"
    response = requests.post(url, json=trial)
    if response.ok:
        return response.json()
    else:
        print("Error pushing trial:", response.status_code, response.text)
        return None

def fetch_persona(persona_id):
    url = f"{CONVEX_URL}/functions/get/persona/{persona_id}"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        print("Error fetching persona:", response.status_code, response.text)
        return None

def fetch_trial(trial_id):
    url = f"{CONVEX_URL}/functions/get/trial/{trial_id}"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        print("Error fetching trial:", response.status_code, response.text)
        return None
