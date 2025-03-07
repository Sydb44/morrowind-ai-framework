#!/usr/bin/env python3
# Morrowind AI Framework - Context Manager

import json
import logging
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

logger = logging.getLogger(__name__)

@dataclass
class NPCContext:
    """NPC context including personality, memory, and conversation history."""
    
    id: str
    name: str
    race: str = "Unknown"
    gender: str = "Unknown"
    class_type: str = "Unknown"
    faction: str = "None"
    personality: str = ""
    background: str = ""
    goals: str = ""
    conversations: List[Dict[str, Any]] = field(default_factory=list)
    events: List[Dict[str, Any]] = field(default_factory=list)
    disposition: int = 50
    last_interaction: int = field(default_factory=lambda: int(time.time()))
    
    def add_conversation(self, player_message: str, npc_response: str):
        """
        Add a conversation to the NPC's memory.
        
        Args:
            player_message: Player's message
            npc_response: NPC's response
        """
        timestamp = int(time.time())
        self.conversations.append({
            "timestamp": timestamp,
            "player": player_message,
            "npc": npc_response
        })
        self.last_interaction = timestamp
        
        # Limit conversation history
        if len(self.conversations) > 10:
            self.conversations.pop(0)
    
    def add_event(self, event_type: str, description: Any):
        """
        Add an event to the NPC's memory.
        
        Args:
            event_type: Type of event
            description: Event description
        """
        timestamp = int(time.time())
        self.events.append({
            "timestamp": timestamp,
            "type": event_type,
            "description": description
        })
        self.last_interaction = timestamp
        
        # Limit event history
        if len(self.events) > 20:
            self.events.pop(0)
    
    def update_memory(self, memory: Dict[str, Any]):
        """
        Update the NPC's memory from a dictionary.
        
        Args:
            memory: Memory dictionary
        """
        if "conversations" in memory:
            self.conversations = memory["conversations"]
        if "events" in memory:
            self.events = memory["events"]
        if "disposition" in memory:
            self.disposition = memory["disposition"]
        if "last_interaction" in memory:
            self.last_interaction = memory["last_interaction"]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the NPC context to a dictionary.
        
        Returns:
            Dictionary representation of the NPC context
        """
        return {
            "id": self.id,
            "name": self.name,
            "race": self.race,
            "gender": self.gender,
            "class": self.class_type,
            "faction": self.faction,
            "personality": self.personality,
            "background": self.background,
            "goals": self.goals,
            "conversations": self.conversations,
            "events": self.events,
            "disposition": self.disposition,
            "last_interaction": self.last_interaction
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NPCContext":
        """
        Create an NPC context from a dictionary.
        
        Args:
            data: Dictionary representation of the NPC context
            
        Returns:
            NPC context
        """
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            race=data.get("race", "Unknown"),
            gender=data.get("gender", "Unknown"),
            class_type=data.get("class", "Unknown"),
            faction=data.get("faction", "None"),
            personality=data.get("personality", ""),
            background=data.get("background", ""),
            goals=data.get("goals", ""),
            conversations=data.get("conversations", []),
            events=data.get("events", []),
            disposition=data.get("disposition", 50),
            last_interaction=data.get("last_interaction", int(time.time()))
        )

class ContextManager:
    """Manager for NPC contexts."""
    
    def __init__(self, config):
        """
        Initialize the context manager.
        
        Args:
            config: Server configuration
        """
        self.config = config
        self.npc_profiles_path = config.paths.npc_profiles
        self.memories_path = config.paths.memories
        self.npc_contexts: Dict[str, NPCContext] = {}
        
        # Create directories if they don't exist
        os.makedirs(self.npc_profiles_path, exist_ok=True)
        os.makedirs(self.memories_path, exist_ok=True)
    
    def get_npc_context(self, npc_id: str, npc_data: Optional[Dict[str, Any]] = None) -> NPCContext:
        """
        Get or create an NPC context.
        
        Args:
            npc_id: NPC ID
            npc_data: NPC data (optional)
            
        Returns:
            NPC context
        """
        # Check if context is already loaded
        if npc_id in self.npc_contexts:
            return self.npc_contexts[npc_id]
        
        # Try to load context from memory file
        memory_path = Path(self.memories_path) / f"{npc_id}.json"
        if memory_path.exists():
            try:
                with open(memory_path, "r") as f:
                    memory_data = json.load(f)
                context = NPCContext.from_dict(memory_data)
                self.npc_contexts[npc_id] = context
                logger.info(f"Loaded memory for NPC {npc_id}")
                return context
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error loading memory for NPC {npc_id}: {e}")
        
        # Try to load context from profile file
        profile_path = Path(self.npc_profiles_path) / f"{npc_id}.json"
        if profile_path.exists():
            try:
                with open(profile_path, "r") as f:
                    profile_data = json.load(f)
                context = NPCContext.from_dict(profile_data)
                self.npc_contexts[npc_id] = context
                logger.info(f"Loaded profile for NPC {npc_id}")
                return context
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error loading profile for NPC {npc_id}: {e}")
        
        # Create new context from provided data
        if npc_data:
            context = NPCContext(
                id=npc_id,
                name=npc_data.get("name", ""),
                race=npc_data.get("race", "Unknown"),
                gender=npc_data.get("gender", "Unknown"),
                class_type=npc_data.get("class", "Unknown"),
                faction=npc_data.get("faction", "None")
            )
            self.npc_contexts[npc_id] = context
            logger.info(f"Created new context for NPC {npc_id}")
            return context
        
        # Create empty context
        context = NPCContext(id=npc_id, name=npc_id)
        self.npc_contexts[npc_id] = context
        logger.info(f"Created empty context for NPC {npc_id}")
        return context
    
    def save_npc_context(self, npc_id: str, context: NPCContext):
        """
        Save an NPC context to disk.
        
        Args:
            npc_id: NPC ID
            context: NPC context
        """
        if not self.config.features.memory_persistence:
            return
        
        memory_path = Path(self.memories_path) / f"{npc_id}.json"
        try:
            with open(memory_path, "w") as f:
                json.dump(context.to_dict(), f, indent=2)
            logger.info(f"Saved memory for NPC {npc_id}")
        except Exception as e:
            logger.error(f"Error saving memory for NPC {npc_id}: {e}")
