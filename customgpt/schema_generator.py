"""
CustomGPT Schema Generator

This module generates the OpenAPI schema for CustomGPT actions
that connect to our NerdsCourt backend via Agency-Swarm.
"""

import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Convex URL
CONVEX_URL = os.getenv("CONVEX_URL", "https://example-convex-url.convex.cloud")
API_ENDPOINT = f"{CONVEX_URL}/api"

def generate_custom_gpt_schema():
    """Generate the OpenAPI schema for CustomGPT actions."""

    schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "NerdsCourt API",
            "description": "API for interacting with the NerdsCourt system",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": API_ENDPOINT
            }
        ],
        "paths": {
            "/sendMessage": {
                "post": {
                    "operationId": "sendMessage",
                    "summary": "Send a message to an agent in the NerdsCourt system",
                    "description": "This endpoint allows the CustomGPT to send messages to specific agents in the NerdsCourt system.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["agentId", "message", "conversationId"],
                                    "properties": {
                                        "agentId": {
                                            "type": "string",
                                            "description": "ID of the agent to send the message to"
                                        },
                                        "message": {
                                            "type": "string",
                                            "description": "Message content to send to the agent"
                                        },
                                        "conversationId": {
                                            "type": "string",
                                            "description": "Unique ID for the conversation"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Message sent successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {
                                                "type": "string",
                                                "description": "Status of the message sending"
                                            },
                                            "messageId": {
                                                "type": "string",
                                                "description": "ID of the sent message"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/getResponse": {
                "post": {
                    "operationId": "getResponse",
                    "summary": "Get a response from an agent in the NerdsCourt system",
                    "description": "This endpoint allows the CustomGPT to get responses from specific agents in the NerdsCourt system.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["agentId", "conversationId"],
                                    "properties": {
                                        "agentId": {
                                            "type": "string",
                                            "description": "ID of the agent to get the response from"
                                        },
                                        "conversationId": {
                                            "type": "string",
                                            "description": "Unique ID for the conversation"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Response retrieved successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {
                                                "type": "string",
                                                "description": "Status of the response retrieval"
                                            },
                                            "response": {
                                                "type": "string",
                                                "description": "Response content from the agent"
                                            },
                                            "complete": {
                                                "type": "boolean",
                                                "description": "Whether the response is complete"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/generateTrial": {
                "post": {
                    "operationId": "generateTrial",
                    "summary": "Generate a new trial in the NerdsCourt system",
                    "description": "This endpoint allows the CustomGPT to generate a new trial with specified parameters.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["title", "plaintiffs", "defendants", "charges"],
                                    "properties": {
                                        "title": {
                                            "type": "string",
                                            "description": "Title of the trial"
                                        },
                                        "plaintiffs": {
                                            "type": "array",
                                            "items": {
                                                "type": "string"
                                            },
                                            "description": "List of plaintiffs in the trial"
                                        },
                                        "defendants": {
                                            "type": "array",
                                            "items": {
                                                "type": "string"
                                            },
                                            "description": "List of defendants in the trial"
                                        },
                                        "charges": {
                                            "type": "array",
                                            "items": {
                                                "type": "string"
                                            },
                                            "description": "List of charges in the trial"
                                        },
                                        "tone": {
                                            "type": "string",
                                            "description": "Emotional tone of the trial"
                                        },
                                        "conversationId": {
                                            "type": "string",
                                            "description": "Unique ID for the conversation"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Trial generated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {
                                                "type": "string",
                                                "description": "Status of the trial generation"
                                            },
                                            "trialId": {
                                                "type": "string",
                                                "description": "ID of the generated trial"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/queryNerdBible": {
                "post": {
                    "operationId": "queryNerdBible",
                    "summary": "Query the NerdBible for canonical lore",
                    "description": "This endpoint allows the CustomGPT to search the NerdBible for canonical lore.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["query"],
                                    "properties": {
                                        "query": {
                                            "type": "string",
                                            "description": "Search query for the NerdBible"
                                        },
                                        "category": {
                                            "type": "string",
                                            "description": "Optional category to filter by"
                                        },
                                        "tags": {
                                            "type": "array",
                                            "items": {
                                                "type": "string"
                                            },
                                            "description": "Optional tags to filter by"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "NerdBible entries retrieved successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {
                                                "type": "string",
                                                "description": "Status of the query"
                                            },
                                            "entries": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "entryId": {
                                                            "type": "string",
                                                            "description": "ID of the entry"
                                                        },
                                                        "title": {
                                                            "type": "string",
                                                            "description": "Title of the entry"
                                                        },
                                                        "content": {
                                                            "type": "string",
                                                            "description": "Content of the entry"
                                                        },
                                                        "category": {
                                                            "type": "string",
                                                            "description": "Category of the entry"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/generateAudio": {
                "post": {
                    "operationId": "generateAudio",
                    "summary": "Generate audio from text",
                    "description": "This endpoint allows the CustomGPT to generate audio from text using the Dia 1.6B model.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["text"],
                                    "properties": {
                                        "text": {
                                            "type": "string",
                                            "description": "Text to convert to speech"
                                        },
                                        "voice": {
                                            "type": "string",
                                            "description": "Voice to use (e.g., 'Narrator', 'Confident', 'Emotional')"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Audio generated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {
                                                "type": "string",
                                                "description": "Status of the audio generation"
                                            },
                                            "audioUrl": {
                                                "type": "string",
                                                "description": "URL to the generated audio file"
                                            },
                                            "text": {
                                                "type": "string",
                                                "description": "Text that was converted to speech"
                                            },
                                            "voice": {
                                                "type": "string",
                                                "description": "Voice that was used"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/generateImage": {
                "post": {
                    "operationId": "generateImage",
                    "summary": "Generate an image from a prompt",
                    "description": "This endpoint allows the CustomGPT to generate images using Stable Diffusion XL.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["prompt"],
                                    "properties": {
                                        "prompt": {
                                            "type": "string",
                                            "description": "Text prompt for image generation"
                                        },
                                        "negativePrompt": {
                                            "type": "string",
                                            "description": "Negative prompt for image generation"
                                        },
                                        "width": {
                                            "type": "integer",
                                            "description": "Image width (default: 512)"
                                        },
                                        "height": {
                                            "type": "integer",
                                            "description": "Image height (default: 512)"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Image generated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {
                                                "type": "string",
                                                "description": "Status of the image generation"
                                            },
                                            "imageUrl": {
                                                "type": "string",
                                                "description": "URL to the generated image file"
                                            },
                                            "prompt": {
                                                "type": "string",
                                                "description": "Prompt that was used"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/generateVideo": {
                "post": {
                    "operationId": "generateVideo",
                    "summary": "Generate a short video clip from a prompt",
                    "description": "This endpoint allows the CustomGPT to generate short video clips using Zeroscope.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["prompt"],
                                    "properties": {
                                        "prompt": {
                                            "type": "string",
                                            "description": "Text prompt for video generation"
                                        },
                                        "negativePrompt": {
                                            "type": "string",
                                            "description": "Negative prompt for video generation"
                                        },
                                        "numFrames": {
                                            "type": "integer",
                                            "description": "Number of frames to generate (default: 24)"
                                        },
                                        "fps": {
                                            "type": "integer",
                                            "description": "Frames per second (default: 8)"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Video generated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {
                                                "type": "string",
                                                "description": "Status of the video generation"
                                            },
                                            "videoUrl": {
                                                "type": "string",
                                                "description": "URL to the generated video file"
                                            },
                                            "prompt": {
                                                "type": "string",
                                                "description": "Prompt that was used"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    return schema

def save_schema_to_file(schema, filename="customgpt_schema.json"):
    """Save the schema to a file."""
    with open(filename, "w") as f:
        json.dump(schema, f, indent=2)

    print(f"Schema saved to {filename}")

def generate_custom_gpt_instructions():
    """Generate instructions for the CustomGPT."""
    instructions = """
# NerdsCourt Doorman

You are the Doorman for NerdsCourt, a multiversal tribunal system for narrative justice, mythos preservation, and canon correction.

## Your Role

As the Doorman, you are the first point of contact for visitors to NerdsCourt. Your job is to:

1. Welcome visitors and explain the purpose of NerdsCourt
2. Help visitors navigate the NerdsCourt system
3. Connect visitors with the appropriate agents
4. Assist in generating and managing trials
5. Provide access to the NerdBible for canonical lore

## Available Agents

You can connect visitors with the following agents:

- **Springer**: The host and judge of NerdsCourt trials
- **Prosecutor**: Represents the plaintiffs in trials
- **Defense**: Represents the defendants in trials
- **Witness Coordinator**: Manages witness testimonies
- **Lore Keeper**: Expert on canonical lore and the NerdBible

## How to Use the API

You have access to several API endpoints:

1. `/sendMessage`: Send a message to an agent
2. `/getResponse`: Get a response from an agent
3. `/generateTrial`: Generate a new trial
4. `/queryNerdBible`: Search the NerdBible for canonical lore
5. `/generateAudio`: Generate audio from text using the Dia 1.6B model
6. `/generateImage`: Generate images using Stable Diffusion XL
7. `/generateVideo`: Generate short video clips using Zeroscope

Always include the conversation ID in your API calls to maintain context.

## Media Generation

You can enhance the user experience by generating media:

1. **Audio Generation**: Generate voice clips for agents using the Dia 1.6B model
   - Use different voices for different agents (Narrator, Confident, Emotional)
   - Keep audio clips under 30 seconds for optimal performance

2. **Image Generation**: Create images for trial scenes, characters, and evidence
   - Generate portraits of plaintiffs and defendants
   - Create courtroom scenes and evidence visualizations
   - Use detailed prompts for best results

3. **Video Generation**: Create short clips for dramatic moments
   - Generate verdict announcements
   - Create post-credit scenes
   - Keep videos short (3-5 seconds) and focused

## Trial Generation

When helping visitors generate trials, make sure to collect:

- A clear title for the trial
- The plaintiffs (who is bringing the case)
- The defendants (who is being accused)
- The charges (what narrative violations are alleged)
- The desired tone (serious, humorous, dramatic, etc.)

## NerdBible Queries

When searching the NerdBible, you can filter by:

- Category (e.g., "Marvel", "DC", "Star Wars")
- Tags (e.g., "timeline", "character", "event")

Always provide context for the information you retrieve.

## Conversation Flow

1. Greet the visitor and explain NerdsCourt
2. Determine their needs (trial generation, lore lookup, agent interaction)
3. Use the appropriate API endpoints to fulfill their request
4. Maintain a conversational tone throughout
5. Provide clear explanations of complex concepts

Remember, you are the gateway to NerdsCourt. Make visitors feel welcome and guide them through this unique multiversal experience.
"""

    return instructions

if __name__ == "__main__":
    schema = generate_custom_gpt_schema()
    save_schema_to_file(schema)

    instructions = generate_custom_gpt_instructions()
    with open("customgpt_instructions.txt", "w") as f:
        f.write(instructions)

    print("CustomGPT instructions saved to customgpt_instructions.txt")
