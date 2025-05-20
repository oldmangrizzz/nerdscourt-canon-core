#!/usr/bin/env python3
"""
NerdsCourt Canon Core - Backend Integration

This script serves as the main entry point for the NerdsCourt Canon Core backend,
integrating all the components and providing a unified interface for the frontend.
"""

import os
import json
import argparse
from dotenv import load_dotenv

# Import the core modules
from krakoa_engine.generate_krakoa_persona import generate_krakoa_persona
from trial_logic.trial_forge import generate_trial_record
from backend_bridge.convex_bridge import (
    push_persona_to_convex,
    push_trial_to_convex,
    fetch_persona,
    fetch_trial
)
from swarm_logic.zord_model_router import match_zord_model
from voice_logic.generate_voice import generate_agent_voice

# Load environment variables
load_dotenv()

def create_persona(seed_data):
    """
    Create a persona using the Krakoa Engine and push it to Convex.
    
    Args:
        seed_data (dict): Seed data for persona generation
        
    Returns:
        dict: The created persona with Convex ID
    """
    # Generate the persona using the Krakoa Engine
    persona = generate_krakoa_persona(seed_data)
    
    # Push the persona to Convex
    result = push_persona_to_convex(persona)
    
    if result:
        print(f"Persona created: {persona['identity']['designation']}")
        return result
    else:
        print("Failed to create persona")
        return None

def create_trial(trial_data):
    """
    Create a trial using the Trial Forge and push it to Convex.
    
    Args:
        trial_data (dict): Trial data including title, plaintiffs, defendants, charges
        
    Returns:
        dict: The created trial with Convex ID
    """
    # Extract the required fields
    title = trial_data.get("title", "Untitled Trial")
    plaintiffs = trial_data.get("plaintiffs", [])
    defendants = trial_data.get("defendants", [])
    charges = trial_data.get("charges", [])
    tone = trial_data.get("trial_tone", "lore satire")
    linked_record = trial_data.get("linked_record", None)
    
    # Generate the trial record
    trial = generate_trial_record(
        title=title,
        plaintiffs=plaintiffs,
        defendants=defendants,
        charges=charges,
        tone=tone,
        linked_record=linked_record
    )
    
    # Push the trial to Convex
    result = push_trial_to_convex(trial)
    
    if result:
        print(f"Trial created: {trial['title']}")
        return result
    else:
        print("Failed to create trial")
        return None

def get_model_for_agent(agent_data):
    """
    Get the appropriate model for an agent using the Zord Model Router.
    
    Args:
        agent_data (dict): Agent data
        
    Returns:
        str: The model identifier
    """
    return match_zord_model(agent_data)

def generate_voice_line(text, audio_prompt_url=None):
    """
    Generate a voice line using the Voice Logic.
    
    Args:
        text (str): The text to convert to speech
        audio_prompt_url (str, optional): URL to an audio prompt
        
    Returns:
        str: URL to the generated audio
    """
    return generate_agent_voice(text, audio_prompt_url)

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="NerdsCourt Canon Core Backend")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Create persona command
    persona_parser = subparsers.add_parser("create-persona", help="Create a new persona")
    persona_parser.add_argument("--file", help="JSON file with persona seed data")
    persona_parser.add_argument("--name", help="Name of the persona")
    persona_parser.add_argument("--alias", help="Alias of the persona")
    persona_parser.add_argument("--universe", help="Universe of the persona")
    persona_parser.add_argument("--spawned-from", help="Origin of the persona")
    
    # Create trial command
    trial_parser = subparsers.add_parser("create-trial", help="Create a new trial")
    trial_parser.add_argument("--file", help="JSON file with trial data")
    trial_parser.add_argument("--title", help="Title of the trial")
    trial_parser.add_argument("--plaintiffs", nargs="+", help="Plaintiffs in the trial")
    trial_parser.add_argument("--defendants", nargs="+", help="Defendants in the trial")
    trial_parser.add_argument("--charges", nargs="+", help="Charges in the trial")
    
    # Get model command
    model_parser = subparsers.add_parser("get-model", help="Get model for an agent")
    model_parser.add_argument("--file", help="JSON file with agent data")
    model_parser.add_argument("--persona-id", help="ID of the persona in Convex")
    
    # Generate voice command
    voice_parser = subparsers.add_parser("generate-voice", help="Generate voice for text")
    voice_parser.add_argument("--text", help="Text to convert to speech")
    voice_parser.add_argument("--audio-prompt", help="URL to an audio prompt")
    
    args = parser.parse_args()
    
    if args.command == "create-persona":
        if args.file:
            with open(args.file, "r") as f:
                seed_data = json.load(f)
        else:
            seed_data = {
                "name": args.name or "Unnamed Agent",
                "alias": args.alias or "Undefined Role",
                "universe": args.universe or "Earth-1218",
                "spawned_from": args.spawned_from or "Legacy Initialization",
            }
        
        result = create_persona(seed_data)
        if result:
            print(json.dumps(result, indent=2))
    
    elif args.command == "create-trial":
        if args.file:
            with open(args.file, "r") as f:
                trial_data = json.load(f)
        else:
            trial_data = {
                "title": args.title or "Untitled Trial",
                "plaintiffs": args.plaintiffs or [],
                "defendants": args.defendants or [],
                "charges": args.charges or [],
            }
        
        result = create_trial(trial_data)
        if result:
            print(json.dumps(result, indent=2))
    
    elif args.command == "get-model":
        if args.file:
            with open(args.file, "r") as f:
                agent_data = json.load(f)
            model = get_model_for_agent(agent_data)
            print(f"Model: {model}")
        elif args.persona_id:
            persona = fetch_persona(args.persona_id)
            if persona:
                model = get_model_for_agent(persona)
                print(f"Model: {model}")
            else:
                print("Persona not found")
        else:
            print("Either --file or --persona-id is required")
    
    elif args.command == "generate-voice":
        if args.text:
            audio_url = generate_voice_line(args.text, args.audio_prompt)
            if audio_url:
                print(f"Audio URL: {audio_url}")
            else:
                print("Failed to generate voice")
        else:
            print("--text is required")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
