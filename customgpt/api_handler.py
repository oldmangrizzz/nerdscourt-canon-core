"""
CustomGPT API Handler

This module handles API requests from the CustomGPT and routes them
to the appropriate Agency-Swarm agents and Convex backend.
"""

import os
import json
import uuid
import time
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Agency-Swarm and Convex bridge
from backend_bridge.agency_convex_bridge import ConvexBridge
from trial_logic.trial_forge import generate_trial_record
from media_generation.huggingface_bridge import HuggingFaceBridge

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get API key for authentication
API_KEY = os.getenv("CUSTOMGPT_API_KEY")

# Initialize Convex bridge
convex_bridge = ConvexBridge()

# Initialize HuggingFace bridge
huggingface_bridge = HuggingFaceBridge()

# Dictionary to store agent instances
agent_instances = {}

# Create media directory if it doesn't exist
os.makedirs("media", exist_ok=True)

def authenticate_request():
    """Authenticate the request using API key."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return False

    token = auth_header.split(" ")[1]
    return token == API_KEY

def get_conversation_id():
    """Get the conversation ID from the request headers."""
    # CustomGPT provides a conversation ID in the headers
    conversation_id = request.headers.get("X-Conversation-Id")

    # If not provided, generate a new one
    if not conversation_id:
        conversation_id = str(uuid.uuid4())

    return conversation_id

def get_or_create_agent(agent_id, conversation_id):
    """Get an existing agent instance or create a new one."""
    agent_key = f"{agent_id}_{conversation_id}"

    if agent_key in agent_instances:
        return agent_instances[agent_key]

    # Load agent state from Convex
    agent_state = convex_bridge.load_agent_state(agent_id, conversation_id)

    # TODO: Initialize agent based on agent_id
    # This would be implemented based on your agent architecture

    # For now, return a placeholder
    agent = {
        "id": agent_id,
        "conversation_id": conversation_id,
        "state": agent_state
    }

    agent_instances[agent_key] = agent
    return agent

@app.route("/sendMessage", methods=["POST"])
def send_message():
    """Send a message to an agent."""
    # Authenticate request
    if not authenticate_request():
        return jsonify({"error": "Unauthorized"}), 401

    # Get request data
    data = request.json
    agent_id = data.get("agentId")
    message = data.get("message")
    conversation_id = data.get("conversationId") or get_conversation_id()

    if not agent_id or not message:
        return jsonify({"error": "Missing required parameters"}), 400

    # Get or create agent
    agent = get_or_create_agent(agent_id, conversation_id)

    # TODO: Send message to agent using Agency-Swarm
    # This would be implemented based on your agent architecture

    # For now, return a placeholder
    message_id = str(uuid.uuid4())

    return jsonify({
        "status": "message_sent",
        "messageId": message_id,
        "conversationId": conversation_id
    })

@app.route("/getResponse", methods=["POST"])
def get_response():
    """Get a response from an agent."""
    # Authenticate request
    if not authenticate_request():
        return jsonify({"error": "Unauthorized"}), 401

    # Get request data
    data = request.json
    agent_id = data.get("agentId")
    conversation_id = data.get("conversationId") or get_conversation_id()

    if not agent_id:
        return jsonify({"error": "Missing required parameters"}), 400

    # Get or create agent
    agent = get_or_create_agent(agent_id, conversation_id)

    # TODO: Get response from agent using Agency-Swarm
    # This would be implemented based on your agent architecture

    # For now, return a placeholder
    # In a real implementation, this would check if the agent has completed processing
    # and return the appropriate response

    # Simulate a delay for demonstration purposes
    time.sleep(1)

    return jsonify({
        "status": "response_ready",
        "response": f"This is a response from agent {agent_id}",
        "complete": True,
        "conversationId": conversation_id
    })

@app.route("/generateTrial", methods=["POST"])
def generate_trial():
    """Generate a new trial."""
    # Authenticate request
    if not authenticate_request():
        return jsonify({"error": "Unauthorized"}), 401

    # Get request data
    data = request.json
    title = data.get("title")
    plaintiffs = data.get("plaintiffs", [])
    defendants = data.get("defendants", [])
    charges = data.get("charges", [])
    tone = data.get("tone", "lore satire")
    conversation_id = data.get("conversationId") or get_conversation_id()

    if not title or not plaintiffs or not defendants or not charges:
        return jsonify({"error": "Missing required parameters"}), 400

    # Generate trial record
    try:
        trial_record = generate_trial_record(title, plaintiffs, defendants, charges, tone)

        # Save trial record to Convex
        # TODO: Implement this using Convex mutations

        return jsonify({
            "status": "trial_generated",
            "trialId": trial_record["id"],
            "conversationId": conversation_id,
            "trial": trial_record
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/queryNerdBible", methods=["POST"])
def query_nerdbible():
    """Query the NerdBible for canonical lore."""
    # Authenticate request
    if not authenticate_request():
        return jsonify({"error": "Unauthorized"}), 401

    # Get request data
    data = request.json
    query = data.get("query")
    category = data.get("category")
    tags = data.get("tags", [])

    if not query:
        return jsonify({"error": "Missing required parameters"}), 400

    # Query NerdBible
    # TODO: Implement this using Convex queries

    # For now, return a placeholder
    entries = [
        {
            "entryId": "entry1",
            "title": "Sample Entry",
            "content": f"This is a sample entry matching the query: {query}",
            "category": category or "General",
            "tags": tags or ["sample"]
        }
    ]

    return jsonify({
        "status": "entries_found",
        "entries": entries,
        "count": len(entries)
    })

@app.route("/generateAudio", methods=["POST"])
def generate_audio():
    """Generate audio from text."""
    # Authenticate request
    if not authenticate_request():
        return jsonify({"error": "Unauthorized"}), 401

    # Get request data
    data = request.json
    text = data.get("text")
    voice = data.get("voice", "en_male_deep")

    if not text:
        return jsonify({"error": "Missing required parameters"}), 400

    # Generate audio
    try:
        # Generate a unique filename
        filename = f"audio_{uuid.uuid4()}.mp3"
        output_path = os.path.join("media", filename)

        # Generate audio file
        result = huggingface_bridge.generate_audio(text, voice, output_path)

        if not result:
            return jsonify({"error": "Failed to generate audio"}), 500

        # Return the URL to the audio file
        audio_url = f"/media/{filename}"

        return jsonify({
            "status": "audio_generated",
            "audioUrl": audio_url,
            "text": text,
            "voice": voice
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generateImage", methods=["POST"])
def generate_image():
    """Generate an image from a prompt."""
    # Authenticate request
    if not authenticate_request():
        return jsonify({"error": "Unauthorized"}), 401

    # Get request data
    data = request.json
    prompt = data.get("prompt")
    negative_prompt = data.get("negativePrompt")
    width = data.get("width", 512)
    height = data.get("height", 512)

    if not prompt:
        return jsonify({"error": "Missing required parameters"}), 400

    # Generate image
    try:
        # Generate a unique filename
        filename = f"image_{uuid.uuid4()}.jpg"
        output_path = os.path.join("media", filename)

        # Generate image file
        result = huggingface_bridge.generate_image(
            prompt, negative_prompt, output_path, width, height
        )

        if not result:
            return jsonify({"error": "Failed to generate image"}), 500

        # Return the URL to the image file
        image_url = f"/media/{filename}"

        return jsonify({
            "status": "image_generated",
            "imageUrl": image_url,
            "prompt": prompt
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generateVideo", methods=["POST"])
def generate_video():
    """Generate a short video clip from a prompt."""
    # Authenticate request
    if not authenticate_request():
        return jsonify({"error": "Unauthorized"}), 401

    # Get request data
    data = request.json
    prompt = data.get("prompt")
    negative_prompt = data.get("negativePrompt")
    num_frames = data.get("numFrames", 24)
    fps = data.get("fps", 8)

    if not prompt:
        return jsonify({"error": "Missing required parameters"}), 400

    # Generate video
    try:
        # Generate a unique filename
        filename = f"video_{uuid.uuid4()}.mp4"
        output_path = os.path.join("media", filename)

        # Generate video file
        result = huggingface_bridge.generate_video(
            prompt, negative_prompt, output_path, num_frames, fps
        )

        if not result:
            return jsonify({"error": "Failed to generate video"}), 500

        # Return the URL to the video file
        video_url = f"/media/{filename}"

        return jsonify({
            "status": "video_generated",
            "videoUrl": video_url,
            "prompt": prompt
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/media/<path:filename>")
def serve_media(filename):
    """Serve media files."""
    return send_file(os.path.join("media", filename))

if __name__ == "__main__":
    # Run the Flask app
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
