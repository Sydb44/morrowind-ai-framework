#!/usr/bin/env python3
# Morrowind AI Framework - Configuration Handler

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

@dataclass
class ServerConfig:
    """Server configuration."""
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    log_level: str = "info"

@dataclass
class LLMConfig:
    """LLM configuration."""
    provider: str = "openai"
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 150
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    timeout: int = 30
    local_model: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": False,
        "path": "models/llama-7b",
        "context_length": 2048
    })

@dataclass
class VoiceConfig:
    """Voice configuration."""
    enabled: bool = False
    provider: str = "elevenlabs"
    voice_id: str = "default"
    local_tts: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": False,
        "engine": "espeak",
        "voice": "en"
    })

@dataclass
class MemoryConfig:
    """Memory configuration."""
    max_conversation_history: int = 10
    max_events: int = 20
    summarize_threshold: int = 1000
    persist_to_disk: bool = True

@dataclass
class PathsConfig:
    """Paths configuration."""
    npc_profiles: str = "npc-profiles"
    memories: str = "memories"
    static_data: str = "static-data"
    templates: str = "static-data/templates"
    logs: str = "logs"
    voice_output: str = "voice-output"
    conversation_logs: str = "conversation-logs"

@dataclass
class FeaturesConfig:
    """Features configuration."""
    action_parsing: bool = True
    memory_persistence: bool = True
    conversation_logging: bool = True
    voice_generation: bool = False

@dataclass
class Config:
    """Main configuration class."""
    server: ServerConfig
    llm: LLMConfig
    voice: VoiceConfig
    memory: MemoryConfig
    paths: PathsConfig
    features: FeaturesConfig
    
    def __init__(self, config_dict: Dict[str, Any]):
        """
        Initialize configuration from dictionary.
        
        Args:
            config_dict: Configuration dictionary
        """
        self.server = ServerConfig(**config_dict.get("server", {}))
        self.llm = LLMConfig(**config_dict.get("llm", {}))
        self.voice = VoiceConfig(**config_dict.get("voice", {}))
        self.memory = MemoryConfig(**config_dict.get("memory", {}))
        self.paths = PathsConfig(**config_dict.get("paths", {}))
        self.features = FeaturesConfig(**config_dict.get("features", {}))
        
        # Override with environment variables
        self._override_from_env()
    
    def _override_from_env(self):
        """Override configuration with environment variables."""
        # Server settings
        if host := os.getenv("SERVER_HOST"):
            self.server.host = host
        if port := os.getenv("SERVER_PORT"):
            self.server.port = int(port)
        if log_level := os.getenv("LOG_LEVEL"):
            self.server.log_level = log_level
        
        # LLM settings
        if provider := os.getenv("LLM_PROVIDER"):
            self.llm.provider = provider
        if model := os.getenv("LLM_MODEL"):
            self.llm.model = model
        
        # Local LLM settings
        if path := os.getenv("LOCAL_LLM_PATH"):
            self.llm.local_model["enabled"] = True
            self.llm.local_model["path"] = path
        
        # Voice settings
        if os.getenv("VOICE_ENABLED") == "true":
            self.voice.enabled = True
            self.features.voice_generation = True
        if provider := os.getenv("VOICE_PROVIDER"):
            self.voice.provider = provider
        if voice_id := os.getenv("VOICE_ID"):
            self.voice.voice_id = voice_id

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """
    Load configuration from file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        logger.info(f"Loaded configuration from {config_path}")
        return config
    except FileNotFoundError:
        logger.warning(f"Configuration file {config_path} not found, using default configuration")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in configuration file {config_path}, using default configuration")
        return {}
