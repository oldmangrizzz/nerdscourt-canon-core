# NERDSCOURT Canon Core

This is the living canon archive for the NERDSCOURT multiversal tribunal system. It serves as a centralized memory and modular action repository for a custom GPT-driven narrative engine powered by vibe-coded logic, emotional resonance, and lore accountability.

## Current Files

- `nerdscourt_core_schema.json`: Core system behavior and emotional architecture
- `golden_frame_magneto_prime.json`: Myth-level Magneto event file
- `rdj_affleck_trial_record.json`: Full trial precedent for RDJ & Batfleck
- `intent_map_v1.json`: Natural language command translator
- `README.md`: This doc

## Backend Integration

The backend is now fully integrated with the following components:

- **Krakoa Engine**: Powers persona creation (`krakoa_engine/generate_krakoa_persona.py`)
- **Trial Forge**: Generates trials (`trial_logic/trial_forge.py`)
- **Convex Bridge**: Pushes data to Convex (`backend_bridge/convex_bridge.py`)
- **Zord Model Router**: Matches agent profiles to their ideal model (`swarm_logic/zord_model_router.py`)
- **Voice Logic**: Generates voice lines (`voice_logic/generate_voice.py`)

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   ```
   GITHUB_API_TOKEN=your_github_token
   HUGGINGFACE_API_TOKEN=your_huggingface_token
   CONVEX_DEPLOYMENT_URL=your_convex_url
   OPENROUTER_API_KEY=your_openrouter_key
   ```

3. Initialize Convex (if not already done):
   ```
   npx convex init
   ```

4. Push the Convex schema:
   ```
   npx convex push
   ```

## Usage

### Command Line Interface

The `main.py` script provides a command-line interface for interacting with the backend:

#### Create a Persona

```bash
python main.py create-persona --file agent_profiles/stark_prime.json
```

Or with individual parameters:

```bash
python main.py create-persona --name "Tony Stark" --alias "Iron Man" --universe "Earth-616" --spawned-from "Golden Frame"
```

#### Create a Trial

```bash
python main.py create-trial --file trial_templates/trial_template.json
```

Or with individual parameters:

```bash
python main.py create-trial --title "The Trial of Ultron" --plaintiffs "Vision" "Wanda" --defendants "Ultron" --charges "Genocide" "AI Rebellion"
```

### GPT Integration

From your GPT Builder, instruct your model to:
- Pull JSONs as memory and logic layers
- Interpret natural language into structured calls using `intent_map_v1.json`
- Respect the canon tier of each loaded file

### API Integration

The backend is designed to be integrated with a frontend through the Convex API. The following endpoints are available:

- `spawnPersona`: Create a new persona
- `getPersona`: Get a persona by ID
- `listPersonas`: List all personas
- `generateTrial`: Create a new trial
- `getTrial`: Get a trial by ID
- `listTrials`: List all trials
- `getModelForPersona`: Get the model for a persona

## Status

This repo is actively evolving. Canon grows. Myth expands. Memory matters.

> "Canon is not a democracy. It's a consequence."
