
# zord_model_router.py

def match_zord_model(agent_profile):
    tone = agent_profile.get("emotional_signature", {}).get("tone", "").lower()
    purpose = agent_profile.get("purpose", "").lower()
    traits = agent_profile.get("core_traits", [])
    archetype = agent_profile.get("role", "").lower()

    # Basic keyword heuristics for model matching
    if "trauma" in tone or "sacrifice" in purpose or "legacy" in purpose:
        return "qwen:Qwen3-72B-Instruct"  # Heavy resonance model
    elif "humor" in tone or "chaos" in traits or "meta" in archetype:
        return "openrouter:deepseek-coder"  # Responsive and quirky
    elif "justice" in purpose or "order" in tone or "narrator" in archetype:
        return "openrouter:together-gemma-7b-it"  # Calm rational tone
    elif "evolution" in purpose or "introspection" in tone:
        return "huggingface:deepseek-v2"  # Reflective, scalable
    else:
        return "openrouter:gemini-pro-vision"  # Generalist fallback

# Example usage:
# model = match_zord_model(stark_prime_dict)
