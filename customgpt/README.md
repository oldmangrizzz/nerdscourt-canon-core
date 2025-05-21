# NerdsCourt CustomGPT Integration

This directory contains the code for integrating NerdsCourt with CustomGPT using Agency-Swarm and Convex.

## Overview

The CustomGPT integration provides a conversational interface to the NerdsCourt system, allowing users to:

1. Generate and participate in trials
2. Query the NerdBible for canonical lore
3. Interact with NerdsCourt agents
4. View trial verdicts and sentencing

## Architecture

The integration uses the following components:

- **CustomGPT**: Provides the user interface and natural language understanding
- **Agency-Swarm**: Manages agent communication and orchestration
- **Convex**: Provides the database and backend infrastructure
- **Flask API**: Handles requests from CustomGPT and routes them to the appropriate components

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- Convex account
- OpenAI account with CustomGPT access

### Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   npm install convex
   ```

2. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file to add your API keys and URLs.

3. Deploy Convex functions:
   ```
   npx convex dev
   ```

4. Generate CustomGPT schema:
   ```
   python customgpt/schema_generator.py
   ```

5. Start the API server:
   ```
   python customgpt/api_handler.py
   ```

### Creating the CustomGPT

1. Go to https://chat.openai.com/gpts/editor
2. Create a new GPT named "NerdsCourt Doorman"
3. Copy the instructions from `customgpt/output/customgpt_instructions.txt`
4. Add the schema from `customgpt/output/customgpt_schema.json`
5. Set the API endpoint to your Convex URL
6. Set the API key to the one in your `.env` file

## Usage

Once set up, users can interact with the NerdsCourt system through the CustomGPT interface:

- **Generate a Trial**: "I want to create a trial where Iron Man is suing Batman for stealing his tech"
- **Query the NerdBible**: "Tell me about the canonical timeline of the Marvel Cinematic Universe"
- **Talk to an Agent**: "I'd like to speak with the Prosecutor about my case"
- **View Trial Results**: "Show me the verdict from my recent trial"

## Development

### Adding New Agents

To add a new agent to the system:

1. Create a new agent class in the `agents` directory
2. Register the agent in the `agency_init.py` file
3. Update the CustomGPT instructions to include the new agent

### Adding New API Endpoints

To add a new API endpoint:

1. Add the endpoint to the `api_handler.py` file
2. Update the schema in `schema_generator.py`
3. Regenerate the schema and update the CustomGPT

## Troubleshooting

### Common Issues

- **Authentication Errors**: Check that your API key is correctly set in both the `.env` file and the CustomGPT configuration
- **Missing Responses**: Ensure that the Convex functions are deployed and running
- **Agent Communication Failures**: Check the agent thread storage in Convex

### Logs

Logs are stored in the following locations:

- API server logs: `logs/api.log`
- Convex logs: Available in the Convex dashboard
- Agent logs: Stored in Convex under the `agentLogs` table

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
