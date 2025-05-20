
from datetime import datetime
import uuid

def create_trial_id():
    return f"{uuid.uuid4()}"

def generate_trial_record(title, plaintiffs, defendants, charges, tone="lore satire", linked_record=None):
    timestamp = datetime.utcnow().isoformat() + "Z"
    trial_id = create_trial_id()

    return {
        "case_id": trial_id,
        "title": title,
        "plaintiffs": plaintiffs,
        "defendants": defendants,
        "charges": charges,
        "verdict": "PENDING",
        "sentencing": [],
        "notable_quotes": [],
        "trial_tone": tone,
        "linked_record": linked_record,
        "timestamp": timestamp,
        "post_credit_scene": {
            "setting": "Undetermined",
            "present": [],
            "quote": "TBD"
        }
    }
