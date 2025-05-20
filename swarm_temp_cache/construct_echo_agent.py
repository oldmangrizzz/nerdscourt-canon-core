
import uuid
from datetime import datetime

def create_session_id():
    return f"{int(datetime.now().timestamp())}-{uuid.uuid4()}"

def construct_echo_agent(seed):
    name = seed.get("name", "Echo Construct")
    inspiration = seed.get("inspired_by", "Legacy Performance")
    archetype = seed.get("archetype", "Undefined Role")
    traits = seed.get("traits", ["[Fragment Trait 1]", "[Trait 2]"])
    tone = seed.get("tone", "Respectful Echo")
    core_quote = seed.get("core_quote", "This is not imitation — it is evolution.")
    use_case = seed.get("use_case", "One-time trial or swarm logic node.")

    sid = create_session_id()

    echo = {
        "echo_identity": {
            "designation": name,
            "spawn_type": "echo",
            "inspired_by": inspiration,
            "archetype_base": archetype
        },
        "trait_signature": traits,
        "tone_mapping": tone,
        "core_quote": core_quote,
        "session_id": sid,
        "created_for": use_case,
        "calibrated_by": "Tony Stark Prime",
        "temporary": True,
        "expires": "Post-session unless archived",
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }

    return echo
