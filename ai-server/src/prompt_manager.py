#!/usr/bin/env python3
# Morrowind AI Framework - Prompt Manager

import json
import logging
import os
from pathlib import Path
from string import Template
from typing import Dict, List, Optional, Any, Union

logger = logging.getLogger(__name__)

class PromptManager:
    """Manager for prompt templates and generation."""
    
    def __init__(self, config):
        """
        Initialize the prompt manager.
        
        Args:
            config: Server configuration
        """
        self.config = config
        self.templates_path = config.paths.templates
        self.static_data_path = config.paths.static_data
        
        # Load templates
        self.templates = self._load_templates()
        
        # Load static data
        self.static_data = self._load_static_data()
        
        logger.info(f"Initialized prompt manager with {len(self.templates)} templates")
    
    def _load_templates(self) -> Dict[str, Template]:
        """
        Load prompt templates from files.
        
        Returns:
            Dictionary of templates
        """
        templates = {}
        templates_dir = Path(self.templates_path)
        
        if not templates_dir.exists():
            logger.warning(f"Templates directory {templates_dir} does not exist")
            return templates
        
        for file_path in templates_dir.glob("*.txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    template_text = f.read()
                template_name = file_path.stem
                templates[template_name] = Template(template_text)
                logger.debug(f"Loaded template: {template_name}")
            except Exception as e:
                logger.error(f"Error loading template {file_path}: {e}")
        
        return templates
    
    def _load_static_data(self) -> Dict[str, Any]:
        """
        Load static data from files.
        
        Returns:
            Dictionary of static data
        """
        static_data = {}
        static_data_dir = Path(self.static_data_path)
        
        if not static_data_dir.exists():
            logger.warning(f"Static data directory {static_data_dir} does not exist")
            return static_data
        
        for file_path in static_data_dir.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data_name = file_path.stem
                static_data[data_name] = data
                logger.debug(f"Loaded static data: {data_name}")
            except Exception as e:
                logger.error(f"Error loading static data {file_path}: {e}")
        
        return static_data
    
    def _format_conversation_history(self, context) -> str:
        """
        Format conversation history for inclusion in prompts.
        
        Args:
            context: NPC context
            
        Returns:
            Formatted conversation history
        """
        if not context.conversations:
            return "No previous conversations."
        
        history = []
        for conv in context.conversations:
            timestamp = conv.get("timestamp", "")
            player_msg = conv.get("player", "")
            npc_msg = conv.get("npc", "")
            
            history.append(f"Player: {player_msg}")
            history.append(f"NPC: {npc_msg}")
        
        return "\n".join(history)
    
    def _format_events(self, context) -> str:
        """
        Format events for inclusion in prompts.
        
        Args:
            context: NPC context
            
        Returns:
            Formatted events
        """
        if not context.events:
            return "No notable events."
        
        events = []
        for event in context.events:
            timestamp = event.get("timestamp", "")
            event_type = event.get("type", "")
            description = event.get("description", "")
            
            events.append(f"Event: {event_type}")
            events.append(f"Description: {description}")
        
        return "\n".join(events)
    
    def _get_faction_info(self, faction_name: str) -> str:
        """
        Get information about a faction.
        
        Args:
            faction_name: Faction name
            
        Returns:
            Faction information
        """
        factions = self.static_data.get("factions", {})
        faction = factions.get(faction_name, {})
        
        if not faction:
            return f"No information available for faction: {faction_name}"
        
        return faction.get("description", "")
    
    def _get_location_info(self, location_name: str) -> str:
        """
        Get information about a location.
        
        Args:
            location_name: Location name
            
        Returns:
            Location information
        """
        locations = self.static_data.get("locations", {})
        location = locations.get(location_name, {})
        
        if not location:
            return f"No information available for location: {location_name}"
        
        return location.get("description", "")
    
    def create_dialogue_prompt(self, npc: Dict[str, Any], player_message: str, game_state: Dict[str, Any], context) -> str:
        """
        Create a dialogue prompt for an NPC.
        
        Args:
            npc: NPC data
            player_message: Player's message
            game_state: Game state
            context: NPC context
            
        Returns:
            Dialogue prompt
        """
        # Get dialogue template
        template = self.templates.get("dialogue_template")
        if not template:
            logger.error("Dialogue template not found")
            return f"You are {npc.get('name', 'an NPC')}. Respond to: {player_message}"
        
        # Get faction information
        faction_name = npc.get("faction", "None")
        faction_info = self._get_faction_info(faction_name)
        
        # Get location information
        location_name = game_state.get("location", "Unknown")
        location_info = self._get_location_info(location_name)
        
        # Format conversation history
        conversation_history = self._format_conversation_history(context)
        
        # Format events
        events = self._format_events(context)
        
        # Get lore information
        lore = self.static_data.get("lore", {})
        lore_text = json.dumps(lore, indent=2) if lore else "No lore information available."
        
        # Create template variables
        template_vars = {
            "npc_name": npc.get("name", ""),
            "npc_race": npc.get("race", "Unknown"),
            "npc_gender": npc.get("gender", "Unknown"),
            "npc_class": npc.get("class", "Unknown"),
            "npc_faction": faction_name,
            "npc_faction_info": faction_info,
            "npc_personality": context.personality,
            "npc_background": context.background,
            "npc_goals": context.goals,
            "player_name": game_state.get("player_name", "Outlander"),
            "player_race": game_state.get("player_race", "Unknown"),
            "player_gender": game_state.get("player_gender", "Unknown"),
            "player_class": game_state.get("player_class", "Unknown"),
            "player_faction": game_state.get("player_faction", "None"),
            "location": location_name,
            "location_info": location_info,
            "time_of_day": game_state.get("time_of_day", "Unknown"),
            "weather": game_state.get("weather", "Unknown"),
            "conversation_history": conversation_history,
            "events": events,
            "player_message": player_message,
            "lore": lore_text
        }
        
        # Generate prompt
        try:
            prompt = template.safe_substitute(template_vars)
            return prompt
        except Exception as e:
            logger.error(f"Error generating dialogue prompt: {e}")
            return f"You are {npc.get('name', 'an NPC')}. Respond to: {player_message}"
    
    def create_system_prompt(self) -> str:
        """
        Create a system prompt.
        
        Returns:
            System prompt
        """
        # Get system template
        template = self.templates.get("system_template")
        if not template:
            logger.error("System template not found")
            return "You are a helpful assistant."
        
        # Get lore information
        lore = self.static_data.get("lore", {})
        lore_text = json.dumps(lore, indent=2) if lore else "No lore information available."
        
        # Create template variables
        template_vars = {
            "lore": lore_text
        }
        
        # Generate prompt
        try:
            prompt = template.safe_substitute(template_vars)
            return prompt
        except Exception as e:
            logger.error(f"Error generating system prompt: {e}")
            return "You are a helpful assistant."
