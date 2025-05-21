"""
NerdBible Core Module

This module handles the creation, retrieval, and management of NerdBible entries.
The NerdBible is a living archive of canonical lore and parables, evolving as the project's mythos.
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path

# Ensure the data directory exists
DATA_DIR = Path("data/nerdbible")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Path to the core NerdBible file
NERDBIBLE_CORE_PATH = Path("nerd_bible_core.json")

def load_bible_core():
    """Load the core NerdBible file."""
    try:
        if NERDBIBLE_CORE_PATH.exists():
            with open(NERDBIBLE_CORE_PATH, "r") as f:
                return json.load(f)
        else:
            # Create a default structure if the file doesn't exist
            default_bible = {
                "scripture_core": {
                    "source_type": "canon_only",
                    "inspiration_tiers": ["Golden Frame", "Trial Ruling", "Verified Panel Quote"],
                    "format": "verse + citation",
                    "query_style": "natural language",
                    "response_style": "scriptural and emotionally weighted"
                },
                "entries": []
            }
            with open(NERDBIBLE_CORE_PATH, "w") as f:
                json.dump(default_bible, f, indent=2)
            return default_bible
    except Exception as e:
        print(f"Error loading NerdBible core: {e}")
        return {
            "scripture_core": {
                "source_type": "canon_only",
                "inspiration_tiers": ["Golden Frame", "Trial Ruling", "Verified Panel Quote"],
                "format": "verse + citation",
                "query_style": "natural language",
                "response_style": "scriptural and emotionally weighted"
            },
            "entries": []
        }

def save_bible_core(bible_data):
    """Save the NerdBible core file."""
    try:
        with open(NERDBIBLE_CORE_PATH, "w") as f:
            json.dump(bible_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving NerdBible core: {e}")
        return False

def get_all_entries():
    """Get all NerdBible entries."""
    bible = load_bible_core()
    return bible.get("entries", [])

def get_entry_by_id(entry_id):
    """Get a NerdBible entry by ID."""
    bible = load_bible_core()
    entries = bible.get("entries", [])
    for entry in entries:
        if entry.get("id") == entry_id:
            return entry
    return None

def get_entries_by_theme(theme):
    """Get NerdBible entries by theme."""
    bible = load_bible_core()
    entries = bible.get("entries", [])
    return [entry for entry in entries if entry.get("theme", "").lower() == theme.lower()]

def get_entries_by_character(character):
    """Get NerdBible entries by character."""
    bible = load_bible_core()
    entries = bible.get("entries", [])
    return [entry for entry in entries if entry.get("character", "").lower() == character.lower()]

def create_entry(theme, quote, source, character, tier="Trial Ruling"):
    """Create a new NerdBible entry."""
    bible = load_bible_core()
    entries = bible.get("entries", [])
    
    # Generate a new entry ID
    entry_id = f"NB-{len(entries) + 1:04d}"
    
    # Create the new entry
    new_entry = {
        "id": entry_id,
        "theme": theme,
        "quote": quote,
        "source": source,
        "character": character,
        "tier": tier,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    # Add the entry to the list
    entries.append(new_entry)
    bible["entries"] = entries
    
    # Save the updated Bible
    save_bible_core(bible)
    
    return new_entry

def create_entry_from_trial(trial_data):
    """Create NerdBible entries from a trial record."""
    entries = []
    
    # Extract notable quotes from the trial
    for quote in trial_data.get("notable_quotes", []):
        # Try to extract character and quote text
        parts = quote.split(":", 1)
        if len(parts) == 2:
            character = parts[0].strip()
            quote_text = parts[1].strip().strip('"')
        else:
            character = "Tribunal"
            quote_text = quote.strip().strip('"')
        
        # Create an entry for each quote
        entry = create_entry(
            theme=trial_data.get("charges", ["Justice"])[0].lower(),
            quote=quote_text,
            source=trial_data.get("title", "Untitled Trial"),
            character=character,
            tier="Trial Ruling"
        )
        entries.append(entry)
    
    # Create an entry for the post-credit scene quote if it exists
    post_credit = trial_data.get("post_credit_scene", {})
    if post_credit and post_credit.get("quote"):
        # Use the first present character as the speaker, or "Witness" if none
        character = post_credit.get("present", ["Witness"])[0]
        entry = create_entry(
            theme="reflection",
            quote=post_credit.get("quote"),
            source=f"{trial_data.get('title', 'Untitled Trial')} (Post-Credit)",
            character=character,
            tier="Golden Frame"
        )
        entries.append(entry)
    
    return entries

def search_bible(query):
    """Search the NerdBible for entries matching the query."""
    bible = load_bible_core()
    entries = bible.get("entries", [])
    results = []
    
    query = query.lower()
    for entry in entries:
        # Check if the query appears in any of the entry fields
        if (query in entry.get("theme", "").lower() or
            query in entry.get("quote", "").lower() or
            query in entry.get("source", "").lower() or
            query in entry.get("character", "").lower()):
            results.append(entry)
    
    return results

def get_random_verse():
    """Get a random verse from the NerdBible."""
    import random
    bible = load_bible_core()
    entries = bible.get("entries", [])
    
    if not entries:
        return {
            "id": "NB-0000",
            "theme": "beginning",
            "quote": "The NerdBible awaits its first scripture.",
            "source": "System Initialization",
            "character": "NerdsCourt",
            "tier": "System Message"
        }
    
    return random.choice(entries)

def export_bible_to_json(output_path=None):
    """Export the NerdBible to a JSON file."""
    bible = load_bible_core()
    
    if output_path is None:
        output_path = f"nerdbible_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(output_path, "w") as f:
            json.dump(bible, f, indent=2)
        return output_path
    except Exception as e:
        print(f"Error exporting NerdBible: {e}")
        return None
