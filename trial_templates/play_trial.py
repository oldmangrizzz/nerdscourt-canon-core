
import json
import time
from pathlib import Path
from voice_logic.generate_voice import generate_agent_voice

def play_trial(file_path):
    with open(file_path, "r") as file:
        trial = json.load(file)

    print(f"=== Trial: {trial['title']} ===\nPresiding: {trial['presiding']}\nNarrator: {trial['narrator']}\n")

    for segment in trial["segments"]:
        speaker = segment["speaker"]
        print(f"--- {segment['type'].replace('_', ' ').title()} ({speaker}) ---")
        for line in segment["lines"]:
            print(f"{speaker}: {line}")
            audio_url = generate_agent_voice(line)
            if audio_url:
                print(f"[Voice Output]: {audio_url}")
            time.sleep(2)  # pacing between lines

if __name__ == "__main__":
    # Example usage
    play_trial("nerdscourt-canon-core-main/trial_templates/trial_template.json")
