#!/bin/bash

# NerdsCourt Canon Core Deployment Script

echo "NerdsCourt Canon Core Deployment"
echo "================================"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install git and try again."
    exit 1
fi

# Check if the .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "Created .env file. Please edit it with your actual credentials."
    else
        echo "Error: .env.example not found. Please create a .env file manually."
        exit 1
    fi
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Initialize git if not already initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
fi

# Add all files to git
echo "Adding files to git..."
git add .

# Commit changes
echo "Committing changes..."
read -p "Enter commit message: " commit_message
git commit -m "$commit_message"

# Check if remote origin exists
if ! git remote | grep -q "origin"; then
    echo "Adding remote origin..."
    read -p "Enter GitHub repository URL: " repo_url
    git remote add origin "$repo_url"
fi

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo "Deployment complete!"
echo "Next steps:"
echo "1. Set up Convex: npx convex init"
echo "2. Push Convex schema: npx convex push"
echo "3. Update .env with your Convex deployment URL"

exit 0
