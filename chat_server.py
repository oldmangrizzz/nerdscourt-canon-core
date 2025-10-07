#!/usr/bin/env python3
"""
NerdsCourt Canon Core - Real-time Chat Server

This script provides a WebSocket server for real-time communication
with the NerdsCourt backend.
"""

import asyncio
import websockets
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- NERDSCOURT Engine Integration ---
from krakoa_engine.generate_krakoa_persona import generate_krakoa_persona
from trial_logic.trial_forge import generate_trial_record
from swarm_logic.zord_model_router import match_zord_model
# from voice_logic.generate_voice import generate_agent_voice # Not used in chat yet

async def process_command(command, payload):
    """
    Process a command from the client and return a response.
    """
    if command == "create_persona":
        persona = generate_krakoa_persona(payload)
        return {"status": "success", "data": persona}
    elif command == "create_trial":
        trial = generate_trial_record(
            title=payload.get("title", "Untitled Trial"),
            plaintiffs=payload.get("plaintiffs", []),
            defendants=payload.get("defendants", []),
            charges=payload.get("charges", []),
            tone=payload.get("tone", "lore satire")
        )
        return {"status": "success", "data": trial}
    elif command == "get_model":
        model = match_zord_model(payload)
        return {"status": "success", "data": {"model": model}}
    else:
        return {"status": "error", "message": "Unknown command"}

async def chat_handler(websocket, path):
    """
    Handle incoming WebSocket connections.
    """
    print(f"New connection from {websocket.remote_address}")

    try:
        async for message in websocket:
            print(f"Received message: {message}")

            try:
                data = json.loads(message)
                command = data.get("command")
                payload = data.get("payload", {})

                if command:
                    response = await process_command(command, payload)
                else:
                    response = {"status": "error", "message": "Missing command"}
            except json.JSONDecodeError:
                response = {"status": "error", "message": "Invalid JSON"}
            except Exception as e:
                response = {"status": "error", "message": str(e)}

            await websocket.send(json.dumps(response))
            print(f"Sent response: {json.dumps(response)}")

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print(f"Connection from {websocket.remote_address} closed.")

async def main():
    """
    Start the WebSocket server.
    """
    host = "localhost"
    port = 8765

    async with websockets.serve(chat_handler, host, port):
        print(f"WebSocket server started at ws://{host}:{port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")