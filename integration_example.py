#!/usr/bin/env python3
"""
NerdsCourt Canon Core - Integration Example

This script demonstrates how to use the backend components together.
"""

import os
import json
from dotenv import load_dotenv

# Import the core modules
from krakoa_engine.generate_krakoa_persona import generate_krakoa_persona
from trial_logic.trial_forge import generate_trial_record
from backend_bridge.convex_bridge import push_persona_to_convex, push_trial_to_convex
from swarm_logic.zord_model_router import match_zord_model
from voice_logic.generate_voice import generate_agent_voice

# Load environment variables
load_dotenv()

def integration_example():
    """Run an integration example using all backend components."""
    print("NerdsCourt Canon Core - Integration Example")
    print("==========================================")
    
    # Step 1: Generate a persona using the Krakoa Engine
    print("\n=== Step 1: Generate Persona ===")
    
    seed_data = {
        "name": "Integration Test Agent",
        "alias": "Test Subject Alpha",
        "universe": "Integration-Test-Universe",
        "spawned_from": "Integration Test",
        "traits": ["Integrated", "Tested", "Functional"],
        "purpose": "To demonstrate the integration of backend components",
        "parable": "The parts that work together create a whole greater than their sum."
    }
    
    persona = generate_krakoa_persona(seed_data)
    print(f"Persona generated: {persona['identity']['designation']}")
    
    # Step 2: Match the persona to a model using the Zord Model Router
    print("\n=== Step 2: Match Model ===")
    
    model = persona['model_profile']  # Already matched in generate_krakoa_persona
    print(f"Model matched: {model}")
    
    # Step 3: Generate a trial using the Trial Forge
    print("\n=== Step 3: Generate Trial ===")
    
    title = "The Integration Test Trial"
    plaintiffs = ["Backend Component A", "Backend Component B"]
    defendants = ["Bug", "Error", "Inconsistency"]
    charges = ["Failure to Integrate", "API Mismatch", "Data Corruption"]
    tone = "technical assessment"
    
    trial = generate_trial_record(title, plaintiffs, defendants, charges, tone)
    print(f"Trial generated: {trial['title']}")
    
    # Step 4: Generate a voice line using the Voice Logic
    print("\n=== Step 4: Generate Voice ===")
    
    text = "Integration test complete. All systems operational."
    
    # Note: This will only work if HUGGINGFACE_API_TOKEN is set
    if os.getenv("HUGGINGFACE_API_TOKEN"):
        audio_url = generate_agent_voice(text)
        if audio_url:
            print(f"Voice generated: {audio_url}")
        else:
            print("Voice generation failed. Check the HuggingFace API token.")
    else:
        print("Skipping voice generation. HUGGINGFACE_API_TOKEN not set.")
    
    # Step 5: Push data to Convex (if configured)
    print("\n=== Step 5: Push to Convex ===")
    
    if os.getenv("CONVEX_DEPLOYMENT_URL"):
        # Push persona to Convex
        persona_result = push_persona_to_convex(persona)
        if persona_result:
            print(f"Persona pushed to Convex: {persona_result.get('id', 'Unknown ID')}")
        else:
            print("Failed to push persona to Convex.")
        
        # Push trial to Convex
        trial_result = push_trial_to_convex(trial)
        if trial_result:
            print(f"Trial pushed to Convex: {trial_result.get('id', 'Unknown ID')}")
        else:
            print("Failed to push trial to Convex.")
    else:
        print("Skipping Convex integration. CONVEX_DEPLOYMENT_URL not set.")
    
    print("\n=== Integration Example Complete ===")
    print("All backend components have been demonstrated.")
    print("Check the output above for any errors or warnings.")

if __name__ == "__main__":
    integration_example()
