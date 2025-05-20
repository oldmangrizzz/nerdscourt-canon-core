#!/usr/bin/env python3
"""
NerdsCourt Canon Core - Backend Test Script

This script tests the backend components to ensure they are working correctly.
"""

import os
import json
from dotenv import load_dotenv

# Import the core modules
from krakoa_engine.generate_krakoa_persona import generate_krakoa_persona
from trial_logic.trial_forge import generate_trial_record
from swarm_logic.zord_model_router import match_zord_model

# Load environment variables
load_dotenv()

def test_krakoa_engine():
    """Test the Krakoa Engine for persona generation."""
    print("\n=== Testing Krakoa Engine ===")
    
    # Test data
    seed_data = {
        "name": "Test Agent",
        "alias": "Test Role",
        "universe": "Test Universe",
        "spawned_from": "Test Origin",
        "traits": ["Test Trait 1", "Test Trait 2", "Test Trait 3"],
        "purpose": "Test Purpose",
        "parable": "Test Parable"
    }
    
    # Generate persona
    try:
        persona = generate_krakoa_persona(seed_data)
        print("✅ Persona generated successfully:")
        print(f"  Name: {persona['identity']['designation']}")
        print(f"  Alias: {persona['identity']['alias']}")
        print(f"  Universe: {persona['identity']['universe']}")
        print(f"  Model: {persona['model_profile']}")
        return True
    except Exception as e:
        print(f"❌ Error generating persona: {str(e)}")
        return False

def test_trial_forge():
    """Test the Trial Forge for trial generation."""
    print("\n=== Testing Trial Forge ===")
    
    # Test data
    title = "Test Trial"
    plaintiffs = ["Test Plaintiff 1", "Test Plaintiff 2"]
    defendants = ["Test Defendant 1", "Test Defendant 2"]
    charges = ["Test Charge 1", "Test Charge 2"]
    tone = "test tone"
    
    # Generate trial
    try:
        trial = generate_trial_record(title, plaintiffs, defendants, charges, tone)
        print("✅ Trial generated successfully:")
        print(f"  Title: {trial['title']}")
        print(f"  Case ID: {trial['case_id']}")
        print(f"  Plaintiffs: {', '.join(trial['plaintiffs'])}")
        print(f"  Defendants: {', '.join(trial['defendants'])}")
        print(f"  Charges: {', '.join(trial['charges'])}")
        return True
    except Exception as e:
        print(f"❌ Error generating trial: {str(e)}")
        return False

def test_zord_model_router():
    """Test the Zord Model Router for model matching."""
    print("\n=== Testing Zord Model Router ===")
    
    # Test data
    test_cases = [
        {
            "name": "Trauma Agent",
            "purpose": "To process trauma and sacrifice",
            "core_traits": ["Wounded", "Resilient", "Wise"],
            "role": "Healer",
            "emotional_signature": {"tone": "somber"}
        },
        {
            "name": "Humor Agent",
            "purpose": "To provide comic relief",
            "core_traits": ["Funny", "Chaos", "Unpredictable"],
            "role": "Jester",
            "emotional_signature": {"tone": "playful"}
        },
        {
            "name": "Justice Agent",
            "purpose": "To uphold justice and order",
            "core_traits": ["Fair", "Stern", "Principled"],
            "role": "Judge",
            "emotional_signature": {"tone": "authoritative"}
        },
        {
            "name": "Evolution Agent",
            "purpose": "To facilitate growth and introspection",
            "core_traits": ["Adaptive", "Thoughtful", "Progressive"],
            "role": "Guide",
            "emotional_signature": {"tone": "contemplative"}
        }
    ]
    
    success = True
    
    for i, test_case in enumerate(test_cases):
        try:
            model = match_zord_model(test_case)
            print(f"✅ Test case {i+1} matched successfully:")
            print(f"  Agent: {test_case['name']}")
            print(f"  Model: {model}")
        except Exception as e:
            print(f"❌ Error matching model for test case {i+1}: {str(e)}")
            success = False
    
    return success

def main():
    """Main entry point for the test script."""
    print("NerdsCourt Canon Core - Backend Test")
    print("====================================")
    
    # Run tests
    krakoa_success = test_krakoa_engine()
    trial_success = test_trial_forge()
    zord_success = test_zord_model_router()
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"Krakoa Engine: {'✅ PASS' if krakoa_success else '❌ FAIL'}")
    print(f"Trial Forge: {'✅ PASS' if trial_success else '❌ FAIL'}")
    print(f"Zord Model Router: {'✅ PASS' if zord_success else '❌ FAIL'}")
    
    if krakoa_success and trial_success and zord_success:
        print("\n✅ All tests passed! The backend components are working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        return 1

if __name__ == "__main__":
    exit(main())
