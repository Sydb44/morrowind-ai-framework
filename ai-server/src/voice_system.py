#!/usr/bin/env python3
# Morrowind AI Framework - Voice System

import asyncio
import logging
import os
import time
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

logger = logging.getLogger(__name__)

class VoiceProvider(ABC):
    """Abstract base class for voice providers."""
    
    def __init__(self, config):
        """
        Initialize the voice provider.
        
        Args:
            config: Server configuration
        """
        self.config = config
    
    @abstractmethod
    async def generate_voice(self, text: str, voice_id: str = None) -> str:
        """
        Generate voice from text.
        
        Args:
            text: Text to convert to speech
            voice_id: Voice ID (optional)
            
        Returns:
            Path to the generated audio file
        """
        pass

class ElevenLabsProvider(VoiceProvider):
    """ElevenLabs API provider."""
    
    def __init__(self, config):
        """
        Initialize the ElevenLabs provider.
        
        Args:
            config: Server configuration
        """
        super().__init__(config)
        
        # Set API key from environment variable
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ElevenLabs API key not found in environment variables")
        
        self.voice_id = config.voice.voice_id
        self.output_dir = config.paths.voice_output
        
        # Import elevenlabs here to avoid dependency issues
        try:
            import elevenlabs
            elevenlabs.set_api_key(self.api_key)
            self.elevenlabs = elevenlabs
        except ImportError:
            logger.error("ElevenLabs package not installed. Please install it with 'pip install elevenlabs'")
            raise
    
    async def generate_voice(self, text: str, voice_id: str = None) -> str:
        """
        Generate voice from text using the ElevenLabs API.
        
        Args:
            text: Text to convert to speech
            voice_id: Voice ID (optional)
            
        Returns:
            Path to the generated audio file
        """
        try:
            # Use provided voice ID or default
            voice_id = voice_id or self.voice_id
            
            # Generate a unique filename
            filename = f"{voice_id}_{uuid.uuid4().hex}.mp3"
            output_path = os.path.join(self.output_dir, filename)
            
            # Run in a thread pool to avoid blocking the event loop
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.elevenlabs.save(
                    self.elevenlabs.generate(
                        text=text,
                        voice=voice_id,
                        model="eleven_monolingual_v1"
                    ),
                    output_path
                )
            )
            
            logger.info(f"Generated voice file: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error generating voice with ElevenLabs: {e}")
            raise

class LocalTTSProvider(VoiceProvider):
    """Local text-to-speech provider."""
    
    def __init__(self, config):
        """
        Initialize the local TTS provider.
        
        Args:
            config: Server configuration
        """
        super().__init__(config)
        
        self.engine = config.voice.local_tts.get("engine", "espeak")
        self.voice = config.voice.local_tts.get("voice", "en")
        self.output_dir = config.paths.voice_output
        
        # Import pyttsx3 here to avoid dependency issues
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('voice', self.voice)
        except ImportError:
            logger.error("pyttsx3 package not installed. Please install it with 'pip install pyttsx3'")
            raise
    
    async def generate_voice(self, text: str, voice_id: str = None) -> str:
        """
        Generate voice from text using a local TTS engine.
        
        Args:
            text: Text to convert to speech
            voice_id: Voice ID (optional)
            
        Returns:
            Path to the generated audio file
        """
        try:
            # Generate a unique filename
            filename = f"local_{uuid.uuid4().hex}.mp3"
            output_path = os.path.join(self.output_dir, filename)
            
            # Run in a thread pool to avoid blocking the event loop
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self._generate_and_save(text, output_path)
            )
            
            logger.info(f"Generated voice file: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error generating voice with local TTS: {e}")
            raise
    
    def _generate_and_save(self, text: str, output_path: str):
        """
        Generate voice and save to file.
        
        Args:
            text: Text to convert to speech
            output_path: Output file path
        """
        self.tts_engine.save_to_file(text, output_path)
        self.tts_engine.runAndWait()

class VoiceSystem:
    """System for generating voice from text."""
    
    def __init__(self, config):
        """
        Initialize the voice system.
        
        Args:
            config: Server configuration
        """
        self.config = config
        self.enabled = config.features.voice_generation
        
        if not self.enabled:
            logger.info("Voice generation is disabled")
            return
        
        # Create output directory
        os.makedirs(config.paths.voice_output, exist_ok=True)
        
        # Initialize provider
        self.provider_name = config.voice.provider
        self.provider = self.get_provider(self.provider_name)
        
        logger.info(f"Initialized voice system with provider: {self.provider_name}")
    
    def get_provider(self, provider_name: str) -> VoiceProvider:
        """
        Get a voice provider by name.
        
        Args:
            provider_name: Provider name
            
        Returns:
            Voice provider
        """
        if provider_name == "elevenlabs":
            return ElevenLabsProvider(self.config)
        elif provider_name == "local":
            return LocalTTSProvider(self.config)
        else:
            raise ValueError(f"Unknown voice provider: {provider_name}")
    
    async def generate_voice(self, text: str, npc_id: str = None) -> Optional[str]:
        """
        Generate voice from text.
        
        Args:
            text: Text to convert to speech
            npc_id: NPC ID (optional)
            
        Returns:
            Path to the generated audio file, or None if voice generation is disabled
        """
        if not self.enabled:
            return None
        
        try:
            # Generate voice
            output_path = await self.provider.generate_voice(text, npc_id)
            
            # Return relative path
            return os.path.relpath(output_path, self.config.paths.voice_output)
        except Exception as e:
            logger.error(f"Error generating voice: {e}")
            return None
