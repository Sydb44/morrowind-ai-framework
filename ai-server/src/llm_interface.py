#!/usr/bin/env python3
# Morrowind AI Framework - LLM Interface

import asyncio
import logging
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union

import openai
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, config):
        """
        Initialize the LLM provider.
        
        Args:
            config: Server configuration
        """
        self.config = config
    
    @abstractmethod
    async def generate_text(self, prompt: str, max_tokens: Optional[int] = None, temperature: Optional[float] = None) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Prompt text
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for generation
            
        Returns:
            Generated text
        """
        pass

class OpenAIProvider(LLMProvider):
    """OpenAI API provider."""
    
    def __init__(self, config):
        """
        Initialize the OpenAI provider.
        
        Args:
            config: Server configuration
        """
        super().__init__(config)
        
        # Set API key from environment variable
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        # Set organization if provided
        if org := os.getenv("OPENAI_ORGANIZATION"):
            openai.organization = org
        
        self.model = config.llm.model
        self.temperature = config.llm.temperature
        self.max_tokens = config.llm.max_tokens
        self.top_p = config.llm.top_p
        self.frequency_penalty = config.llm.frequency_penalty
        self.presence_penalty = config.llm.presence_penalty
        self.timeout = config.llm.timeout
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def generate_text(self, prompt: str, max_tokens: Optional[int] = None, temperature: Optional[float] = None) -> str:
        """
        Generate text from a prompt using the OpenAI API.
        
        Args:
            prompt: Prompt text
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for generation
            
        Returns:
            Generated text
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                timeout=self.timeout
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating text with OpenAI: {e}")
            raise

class AnthropicProvider(LLMProvider):
    """Anthropic API provider."""
    
    def __init__(self, config):
        """
        Initialize the Anthropic provider.
        
        Args:
            config: Server configuration
        """
        super().__init__(config)
        
        # Set API key from environment variable
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key not found in environment variables")
        
        self.model = config.llm.model
        self.temperature = config.llm.temperature
        self.max_tokens = config.llm.max_tokens
        self.top_p = config.llm.top_p
        self.timeout = config.llm.timeout
        
        # Import anthropic here to avoid dependency issues
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            logger.error("Anthropic package not installed. Please install it with 'pip install anthropic'")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def generate_text(self, prompt: str, max_tokens: Optional[int] = None, temperature: Optional[float] = None) -> str:
        """
        Generate text from a prompt using the Anthropic API.
        
        Args:
            prompt: Prompt text
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for generation
            
        Returns:
            Generated text
        """
        try:
            response = await self.client.completions.create(
                prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
                model=self.model,
                max_tokens_to_sample=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
                top_p=self.top_p,
                timeout=self.timeout
            )
            
            return response.completion.strip()
        except Exception as e:
            logger.error(f"Error generating text with Anthropic: {e}")
            raise

class LocalLLMProvider(LLMProvider):
    """Local LLM provider."""
    
    def __init__(self, config):
        """
        Initialize the local LLM provider.
        
        Args:
            config: Server configuration
        """
        super().__init__(config)
        
        self.model_path = config.llm.local_model.get("path", "models/llama-7b")
        self.context_length = config.llm.local_model.get("context_length", 2048)
        self.temperature = config.llm.temperature
        self.max_tokens = config.llm.max_tokens
        self.top_p = config.llm.top_p
        
        # Import llama_cpp here to avoid dependency issues
        try:
            from llama_cpp import Llama
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=self.context_length,
                n_threads=os.cpu_count() or 4
            )
        except ImportError:
            logger.error("llama-cpp-python package not installed. Please install it with 'pip install llama-cpp-python'")
            raise
    
    async def generate_text(self, prompt: str, max_tokens: Optional[int] = None, temperature: Optional[float] = None) -> str:
        """
        Generate text from a prompt using a local LLM.
        
        Args:
            prompt: Prompt text
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for generation
            
        Returns:
            Generated text
        """
        try:
            # Run in a thread pool to avoid blocking the event loop
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.llm.create_completion(
                    prompt,
                    max_tokens=max_tokens or self.max_tokens,
                    temperature=temperature or self.temperature,
                    top_p=self.top_p,
                    stop=["Human:", "Assistant:"]
                )
            )
            
            return response["choices"][0]["text"].strip()
        except Exception as e:
            logger.error(f"Error generating text with local LLM: {e}")
            raise

class LLMInterface:
    """Interface for interacting with language models."""
    
    def __init__(self, config):
        """
        Initialize the LLM interface.
        
        Args:
            config: Server configuration
        """
        self.config = config
        self.provider_name = config.llm.provider
        self.provider = self.get_provider(self.provider_name)
        
        logger.info(f"Initialized LLM interface with provider: {self.provider_name}")
    
    def get_provider(self, provider_name: str) -> LLMProvider:
        """
        Get an LLM provider by name.
        
        Args:
            provider_name: Provider name
            
        Returns:
            LLM provider
        """
        if provider_name == "openai":
            return OpenAIProvider(self.config)
        elif provider_name == "anthropic":
            return AnthropicProvider(self.config)
        elif provider_name == "local":
            return LocalLLMProvider(self.config)
        else:
            raise ValueError(f"Unknown LLM provider: {provider_name}")
    
    async def generate_text(self, prompt: str, max_tokens: Optional[int] = None, temperature: Optional[float] = None) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Prompt text
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for generation
            
        Returns:
            Generated text
        """
        # Log prompt if in debug mode
        if self.config.server.debug:
            logger.debug(f"Prompt: {prompt}")
        
        # Generate text
        response = await self.provider.generate_text(prompt, max_tokens, temperature)
        
        # Log response if in debug mode
        if self.config.server.debug:
            logger.debug(f"Response: {response}")
        
        return response
