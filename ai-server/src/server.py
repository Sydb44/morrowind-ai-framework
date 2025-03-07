#!/usr/bin/env python3
# Morrowind AI Framework - AI Server

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Set

import websockets
from websockets.server import WebSocketServerProtocol

from config import Config
from context_manager import ContextManager
from llm_interface import LLMInterface
from prompt_manager import PromptManager
from action_parser import ActionParser
from voice_system import VoiceSystem

logger = logging.getLogger(__name__)

class AIServer:
    """
    WebSocket server for the Morrowind AI Framework.
    Handles connections from the OpenMW client and processes dialogue requests.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the AI server.
        
        Args:
            config: Server configuration
        """
        self.config = Config(config)
        self.host = self.config.server.host
        self.port = self.config.server.port
        self.debug = self.config.server.debug
        
        # Initialize components
        self.llm_interface = LLMInterface(self.config)
        self.prompt_manager = PromptManager(self.config)
        self.context_manager = ContextManager(self.config)
        self.action_parser = ActionParser(self.config)
        
        # Initialize voice system if enabled
        self.voice_system = None
        if self.config.features.voice_generation:
            self.voice_system = VoiceSystem(self.config)
        
        # WebSocket server
        self.server = None
        self.connections: Set[WebSocketServerProtocol] = set()
        
        # Create necessary directories
        self._create_directories()
        
        logger.info(f"AI Server initialized with config: {self.config}")
    
    def _create_directories(self):
        """Create necessary directories for the server."""
        # Create directories for all path attributes in the PathsConfig class
        paths_config = self.config.paths
        for attr_name in dir(paths_config):
            # Skip private attributes and methods
            if attr_name.startswith('_') or callable(getattr(paths_config, attr_name)):
                continue
            
            path = getattr(paths_config, attr_name)
            if isinstance(path, str):
                os.makedirs(path, exist_ok=True)
                logger.debug(f"Created directory: {path}")
    
    async def start(self):
        """Start the WebSocket server."""
        # Log the port we're trying to use
        logger.info(f"Attempting to start server on ws://{self.host}:{self.port}")
        
        self.server = await websockets.serve(
            self._handle_connection,
            self.host,
            self.port
        )
        logger.info(f"Server started on ws://{self.host}:{self.port}")
    
    async def stop(self):
        """Stop the WebSocket server."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            logger.info("Server stopped")
    
    async def _handle_connection(self, websocket: WebSocketServerProtocol, path: str = "/"):
        """
        Handle a new WebSocket connection.
        
        Args:
            websocket: WebSocket connection
            path: Connection path (optional, defaults to "/")
        """
        client_info = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"New connection from {client_info}")
        
        # Add connection to set
        self.connections.add(websocket)
        
        try:
            async for message in websocket:
                try:
                    # Parse message
                    data = json.loads(message)
                    logger.debug(f"Received message: {data}")
                    
                    # Process message based on type
                    if data.get("type") == "dialogue":
                        response = await self._handle_dialogue(data)
                    elif data.get("type") == "event":
                        response = await self._handle_event(data)
                    else:
                        response = {
                            "type": "error",
                            "error": f"Unknown message type: {data.get('type')}",
                            "code": 400
                        }
                    
                    # Send response
                    await websocket.send(json.dumps(response))
                    
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON: {message}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "error": "Invalid JSON",
                        "code": 400
                    }))
                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)
                    await websocket.send(json.dumps({
                        "type": "error",
                        "error": str(e),
                        "code": 500
                    }))
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Connection closed from {client_info}")
        finally:
            # Remove connection from set
            self.connections.remove(websocket)
    
    async def _handle_dialogue(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a dialogue request.
        
        Args:
            data: Dialogue request data
            
        Returns:
            Dialogue response
        """
        # Extract NPC information
        npc = data.get("npc", {})
        npc_id = npc.get("id")
        
        if not npc_id:
            return {
                "type": "error",
                "error": "Missing NPC ID",
                "code": 400
            }
        
        # Get player message
        player_message = data.get("playerMessage", "")
        
        # Get game state
        game_state = data.get("gameState", {})
        
        # Get or create NPC context
        context = self.context_manager.get_npc_context(npc_id, npc)
        
        # Update context with memory from request
        if "memory" in data:
            context.update_memory(data["memory"])
        
        # Generate prompt
        prompt = self.prompt_manager.create_dialogue_prompt(
            npc=npc,
            player_message=player_message,
            game_state=game_state,
            context=context
        )
        
        # Generate response from LLM
        llm_response = await self.llm_interface.generate_text(prompt)
        
        # Parse actions from response
        text, actions = self.action_parser.parse_dialogue_response(llm_response)
        
        # Generate voice if enabled
        voice_path = None
        if self.voice_system and self.config.features.voice_generation:
            voice_path = await self.voice_system.generate_voice(text, npc_id)
        
        # Update NPC memory
        context.add_conversation(player_message, text)
        self.context_manager.save_npc_context(npc_id, context)
        
        # Create response
        response = {
            "type": "dialogue",
            "npc": {
                "id": npc_id,
                "name": npc.get("name", "")
            },
            "text": text,
            "actions": actions
        }
        
        # Add voice path if available
        if voice_path:
            response["voice"] = voice_path
        
        return response
    
    async def _handle_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle an event request.
        
        Args:
            data: Event request data
            
        Returns:
            Event response
        """
        # Extract event information
        npc_id = data.get("npcId")
        event_type = data.get("eventType")
        description = data.get("description")
        
        if not npc_id:
            return {
                "type": "error",
                "error": "Missing NPC ID",
                "code": 400
            }
        
        if not event_type:
            return {
                "type": "error",
                "error": "Missing event type",
                "code": 400
            }
        
        # Get NPC context
        context = self.context_manager.get_npc_context(npc_id)
        
        # Add event to context
        context.add_event(event_type, description)
        
        # Save context
        self.context_manager.save_npc_context(npc_id, context)
        
        # Create response
        return {
            "type": "event_ack",
            "npcId": npc_id,
            "eventType": event_type,
            "status": "success"
        }
