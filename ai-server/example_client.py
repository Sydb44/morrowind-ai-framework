#!/usr/bin/env python3
# Morrowind AI Framework - Example WebSocket Client

import asyncio
import json
import logging
import sys
import websockets
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("example_client")

# Server URL
SERVER_URL = "ws://localhost:8082"

async def send_dialogue_request():
    """Send a dialogue request to the server."""
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            # Create dialogue request
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
            
            # Send request
            logger.info(f"Sending dialogue request: {dialogue_request}")
            await websocket.send(json.dumps(dialogue_request))
            
            # Receive response
            response = await websocket.recv()
            response_data = json.loads(response)
            
            # Print response
            print("\n=== Dialogue Response ===")
            print(f"NPC: {response_data['text']}")
            if "actions" in response_data and response_data["actions"]:
                print("\nActions:")
                for action in response_data["actions"]:
                    print(f"- {action['type']}: {action['params']}")
            
            return response_data
    except Exception as e:
        logger.error(f"Error sending dialogue request: {e}")
        return None

async def send_event_request():
    """Send an event request to the server."""
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            # Create event request
            event_request = {
                "type": "event",
                "npcId": "example_npc",
                "eventType": "PLAYER_JOINED_FACTION",
                "description": "The player has joined House Hlaalu and is now a Retainer."
            }
            
            # Send request
            logger.info(f"Sending event request: {event_request}")
            await websocket.send(json.dumps(event_request))
            
            # Receive response
            response = await websocket.recv()
            response_data = json.loads(response)
            
            # Print response
            print("\n=== Event Response ===")
            print(f"Status: {response_data['status']}")
            
            return response_data
    except Exception as e:
        logger.error(f"Error sending event request: {e}")
        return None

async def interactive_mode():
    """Run the client in interactive mode."""
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            print("\n=== Interactive Mode ===")
            print("Connected to server. Type 'exit' to quit.")
            print("Enter your message to the NPC:")
            
            while True:
                # Get user input
                user_input = input("> ")
                if user_input.lower() == "exit":
                    break
                
                # Create dialogue request
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
                    "playerMessage": user_input,
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
                
                # Send request
                await websocket.send(json.dumps(dialogue_request))
                
                # Receive response
                response = await websocket.recv()
                response_data = json.loads(response)
                
                # Print response
                print(f"\nSedura Ienth: {response_data['text']}")
                if "actions" in response_data and response_data["actions"]:
                    print("\nActions:")
                    for action in response_data["actions"]:
                        print(f"- {action['type']}: {action['params']}")
    except websockets.exceptions.ConnectionClosed:
        print("\nConnection to server closed.")
    except Exception as e:
        logger.error(f"Error in interactive mode: {e}")

async def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        await interactive_mode()
    else:
        # Send dialogue request
        await send_dialogue_request()
        
        # Send event request
        await send_event_request()
        
        print("\nExample client completed. Run with --interactive for interactive mode.")

if __name__ == "__main__":
    asyncio.run(main())
