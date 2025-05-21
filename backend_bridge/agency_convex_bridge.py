"""
Agency-Swarm Convex Bridge

This module provides integration between Agency-Swarm and Convex database.
It handles thread storage, agent state persistence, and communication channels.
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Convex URL and API key
CONVEX_URL = os.getenv("CONVEX_URL")
CONVEX_API_KEY = os.getenv("CONVEX_API_KEY")

class ConvexBridge:
    """Bridge between Agency-Swarm and Convex database."""
    
    def __init__(self, deployment_url=None, api_key=None):
        """
        Initialize the Convex bridge.
        
        Args:
            deployment_url: Convex deployment URL (defaults to env var)
            api_key: Convex API key (defaults to env var)
        """
        self.deployment_url = deployment_url or CONVEX_URL
        self.api_key = api_key or CONVEX_API_KEY
        
        if not self.deployment_url or not self.api_key:
            raise ValueError("Convex URL and API key must be provided")
    
    def _make_request(self, endpoint, method="POST", data=None):
        """Make a request to the Convex API."""
        url = f"{self.deployment_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            if method == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method == "GET":
                response = requests.get(url, headers=headers, params=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to Convex: {e}")
            return None
    
    def save_threads(self, threads_data, conversation_id):
        """
        Save thread data to Convex.
        
        Args:
            threads_data: Thread data to save
            conversation_id: Unique conversation ID
            
        Returns:
            bool: Success status
        """
        # Convert any non-serializable objects to strings
        serialized_data = json.dumps(threads_data, default=str)
        parsed_data = json.loads(serialized_data)
        
        data = {
            "args": {
                "conversationId": conversation_id,
                "threadsData": parsed_data
            }
        }
        
        result = self._make_request("saveAgentThreads", data=data)
        return result is not None
    
    def load_threads(self, conversation_id):
        """
        Load thread data from Convex.
        
        Args:
            conversation_id: Unique conversation ID
            
        Returns:
            dict: Thread data or empty dict if not found
        """
        data = {
            "args": {
                "conversationId": conversation_id
            }
        }
        
        result = self._make_request("getAgentThreads", data=data)
        return result.get("threadsData", {}) if result else {}
    
    def save_agent_state(self, agent_id, state_data, conversation_id):
        """
        Save agent state to Convex.
        
        Args:
            agent_id: Unique agent ID
            state_data: Agent state data
            conversation_id: Conversation context
            
        Returns:
            bool: Success status
        """
        # Convert any non-serializable objects to strings
        serialized_data = json.dumps(state_data, default=str)
        parsed_data = json.loads(serialized_data)
        
        data = {
            "args": {
                "agentId": agent_id,
                "stateData": parsed_data,
                "conversationId": conversation_id
            }
        }
        
        result = self._make_request("saveAgentState", data=data)
        return result is not None
    
    def load_agent_state(self, agent_id, conversation_id):
        """
        Load agent state from Convex.
        
        Args:
            agent_id: Unique agent ID
            conversation_id: Conversation context
            
        Returns:
            dict: Agent state data or empty dict if not found
        """
        data = {
            "args": {
                "agentId": agent_id,
                "conversationId": conversation_id
            }
        }
        
        result = self._make_request("getAgentState", data=data)
        return result.get("stateData", {}) if result else {}

# Convenience functions for Agency-Swarm integration

def save_threads_callback(threads_data, conversation_id):
    """
    Callback function for saving threads in Agency-Swarm.
    
    Args:
        threads_data: Thread data to save
        conversation_id: Unique conversation ID
    
    Returns:
        bool: Success status
    """
    bridge = ConvexBridge()
    return bridge.save_threads(threads_data, conversation_id)

def load_threads_callback(conversation_id):
    """
    Callback function for loading threads in Agency-Swarm.
    
    Args:
        conversation_id: Unique conversation ID
    
    Returns:
        dict: Thread data or empty dict if not found
    """
    bridge = ConvexBridge()
    return bridge.load_threads(conversation_id)
