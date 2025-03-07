#!/usr/bin/env python3
# Morrowind AI Framework - Server Test Script

import asyncio
import json
import logging
import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import server components
from server import AIServer
from config import load_config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("test_server")

async def test_dialogue():
    """Test dialogue generation."""
    # Load configuration
    config = load_config()
    
    # Create server
    server = AIServer(config)
    
    # Test dialogue
    dialogue_request = {
        "type": "dialogue",
        "npc": {
            "id": "example_npc",
            "name": "Sedura Ienth",
            "race": "Dunmer",
            "gender": "Male",
            "class": "Spellsword",
            "faction": "House Hlaalu"
        },
        "playerMessage": "Greetings, I'm new to Balmora. Can you tell me about House Hlaalu?",
        "gameState": {
            "player_name": "Outlander",
            "player_race": "Imperial",
            "player_gender": "Male",
            "player_class": "Warrior",
            "player_faction": "Imperial Legion",
            "location": "Balmora",
            "time_of_day": "Afternoon",
            "weather": "Clear"
        }
    }
    
    # Process dialogue request
    response = await server._handle_dialogue(dialogue_request)
    
    # Print response
    print("\n=== Dialogue Test ===")
    print(f"Player: {dialogue_request['playerMessage']}")
    print(f"NPC: {response['text']}")
    if "actions" in response and response["actions"]:
        print("\nActions:")
        for action in response["actions"]:
            print(f"- {action['type']}: {action['params']}")
    
    return response

async def test_event():
    """Test event handling."""
    # Load configuration
    config = load_config()
    
    # Create server
    server = AIServer(config)
    
    # Test event
    event_request = {
        "type": "event",
        "npcId": "example_npc",
        "eventType": "PLAYER_JOINED_FACTION",
        "description": "The player has joined House Hlaalu and is now a Retainer."
    }
    
    # Process event request
    response = await server._handle_event(event_request)
    
    # Print response
    print("\n=== Event Test ===")
    print(f"Event: {event_request['eventType']}")
    print(f"Description: {event_request['description']}")
    print(f"Response: {response}")
    
    return response

async def main():
    """Main test function."""
    try:
        # Test dialogue
        await test_dialogue()
        
        # Test event
        await test_event()
        
        print("\nAll tests completed successfully!")
    except Exception as e:
        logger.error(f"Error during tests: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
