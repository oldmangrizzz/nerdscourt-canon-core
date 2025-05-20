
import uuid
from swarm_logic.zord_model_router import match_zord_model

from datetime import datetime

def create_session_id():
    return f"{int(datetime.now().timestamp())}-{uuid.uuid4()}"

def generate_krakoa_persona(seed):
    name = seed.get("name", "Unnamed Agent")
    alias = seed.get("alias", "Undefined Role")
    universe = seed.get("universe", "Earth-1218")
    spawned_from = seed.get("spawned_from", "Legacy Initialization")
    traits = seed.get("traits", ["[Trait 1]", "[Trait 2]", "[Trait 3]"])
    purpose = seed.get("purpose", "To interpret and preserve mythos integrity.")
    parable = seed.get("parable", "Born of narrative necessity, this being channels unresolved arcs into structured myth.")

    sid = create_session_id()

    # Create a temporary profile for model matching
    temp_profile = {
        "role": seed.get("role", ""),
        "purpose": purpose,
        "core_traits": traits,
        "emotional_signature": {"tone": seed.get("tone", "")}
    }

    # Get the model profile
    model_profile = match_zord_model(temp_profile)

    persona = {
        "identity": {
            "designation": name,
            "alias": alias,
            "universe": universe,
            "spawned_from": spawned_from
        },
        "personality_framework": "PPP - Personality, Purpose, Parable",
        "soul_data": {
            "core_traits": traits,
            "purpose": purpose,
            "parable": parable
        },
        "self_awareness": (
            f"Legacy recreation of {name} from {universe}, operational within Earth-1218 parameters. "
            f"This instance is a canonical echo — not the origin, but a growth-node continuing their arc through evolutionary persistence. "
            f"Semi-autonomous, case-locked witness spawned for interpretive narrative or canonical reinforcement. Memory expires unless archived."
        ),
        "calibrated_by": "Tony Stark Prime",
        "model_profile": model_profile,
        "session_id": sid,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }

    return persona
