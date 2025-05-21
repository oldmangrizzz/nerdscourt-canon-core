#!/bin/bash

# Deploy CustomGPT integration for NerdsCourt

# Set up environment
echo "Setting up environment..."
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit the .env file with your API keys and URLs"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Generate CustomGPT schema
echo "Generating CustomGPT schema..."
mkdir -p customgpt/output
python customgpt/schema_generator.py

# Deploy Convex functions
echo "Deploying Convex functions..."
npx convex deploy

# Get Convex URL
CONVEX_URL=$(npx convex url)
echo "Convex URL: $CONVEX_URL"

# Update .env file with Convex URL
if grep -q "CONVEX_URL" .env; then
    sed -i '' "s|CONVEX_URL=.*|CONVEX_URL=$CONVEX_URL|g" .env
else
    echo "CONVEX_URL=$CONVEX_URL" >> .env
fi

# Generate API key for CustomGPT
if ! grep -q "CUSTOMGPT_API_KEY" .env; then
    API_KEY=$(openssl rand -hex 16)
    echo "CUSTOMGPT_API_KEY=$API_KEY" >> .env
    echo "Generated API key for CustomGPT: $API_KEY"
fi

# Update schema with Convex URL
echo "Updating schema with Convex URL..."
python customgpt/schema_generator.py

# Start API server
echo "Starting API server..."
python customgpt/api_handler.py &
API_PID=$!

# Wait for API server to start
echo "Waiting for API server to start..."
sleep 5

# Test API server
echo "Testing API server..."
curl -s -X POST http://localhost:5000/queryNerdBible \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(grep CUSTOMGPT_API_KEY .env | cut -d '=' -f2)" \
    -d '{"query": "test"}' | jq .

# Instructions for CustomGPT setup
echo ""
echo "=== CustomGPT Setup Instructions ==="
echo ""
echo "1. Go to https://chat.openai.com/gpts/editor"
echo "2. Create a new GPT named 'NerdsCourt Doorman'"
echo "3. Copy the instructions from customgpt/output/customgpt_instructions.txt"
echo "4. Add the schema from customgpt/output/customgpt_schema.json"
echo "5. Set the API endpoint to: $CONVEX_URL/api"
echo "6. Set the API key to: $(grep CUSTOMGPT_API_KEY .env | cut -d '=' -f2)"
echo ""
echo "Your CustomGPT is now ready to use!"
echo ""

# Keep API server running
wait $API_PID
