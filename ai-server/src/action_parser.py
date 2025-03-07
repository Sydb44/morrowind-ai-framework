#!/usr/bin/env python3
# Morrowind AI Framework - Action Parser

import json
import logging
import re
from typing import Dict, List, Optional, Any, Tuple, Union

logger = logging.getLogger(__name__)

class ActionParser:
    """Parser for extracting actions from LLM responses."""
    
    def __init__(self, config):
        """
        Initialize the action parser.
        
        Args:
            config: Server configuration
        """
        self.config = config
        self.enabled = config.features.action_parsing
        
        # Define action patterns
        self.action_patterns = [
            # Format: [ACTION_TYPE:param1=value1,param2=value2]
            (r'\[(?P<action_type>[A-Z_]+)(?P<params>:[^]]*?)?\]', self._parse_bracketed_action),
            
            # Format: *ACTION_TYPE: description*
            (r'\*(?P<action_type>[A-Z_]+):\s*(?P<description>[^*]+)\*', self._parse_asterisk_action),
            
            # Format: <ACTION_TYPE>description</ACTION_TYPE>
            (r'<(?P<action_type>[A-Z_]+)>(?P<description>.*?)</\1>', self._parse_xml_action)
        ]
        
        logger.info(f"Initialized action parser (enabled: {self.enabled})")
    
    def _parse_bracketed_action(self, match) -> Dict[str, Any]:
        """
        Parse a bracketed action.
        
        Args:
            match: Regex match object
            
        Returns:
            Action dictionary
        """
        action_type = match.group('action_type')
        params_str = match.group('params')
        
        action = {
            "type": action_type,
            "params": {}
        }
        
        if params_str:
            # Remove the leading colon
            params_str = params_str[1:]
            
            # Parse parameters
            for param in params_str.split(','):
                if '=' in param:
                    key, value = param.split('=', 1)
                    action["params"][key.strip()] = value.strip()
                else:
                    # If no equals sign, treat as a flag parameter
                    action["params"][param.strip()] = True
        
        return action
    
    def _parse_asterisk_action(self, match) -> Dict[str, Any]:
        """
        Parse an asterisk action.
        
        Args:
            match: Regex match object
            
        Returns:
            Action dictionary
        """
        action_type = match.group('action_type')
        description = match.group('description').strip()
        
        action = {
            "type": action_type,
            "params": {
                "description": description
            }
        }
        
        return action
    
    def _parse_xml_action(self, match) -> Dict[str, Any]:
        """
        Parse an XML-style action.
        
        Args:
            match: Regex match object
            
        Returns:
            Action dictionary
        """
        action_type = match.group('action_type')
        description = match.group('description').strip()
        
        action = {
            "type": action_type,
            "params": {
                "description": description
            }
        }
        
        return action
    
    def parse_dialogue_response(self, response: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Parse a dialogue response to extract actions.
        
        Args:
            response: LLM response
            
        Returns:
            Tuple of (cleaned text, list of actions)
        """
        if not self.enabled:
            return response, []
        
        actions = []
        cleaned_text = response
        
        # Extract JSON blocks
        json_pattern = r'```json\s*(.*?)\s*```'
        json_matches = re.finditer(json_pattern, response, re.DOTALL)
        
        for match in json_matches:
            json_str = match.group(1)
            try:
                json_data = json.loads(json_str)
                
                # Check if it's an action or actions
                if isinstance(json_data, dict) and "type" in json_data:
                    actions.append(json_data)
                elif isinstance(json_data, list):
                    for item in json_data:
                        if isinstance(item, dict) and "type" in item:
                            actions.append(item)
                
                # Remove the JSON block from the text
                cleaned_text = cleaned_text.replace(match.group(0), "")
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON: {json_str}")
        
        # Extract actions using patterns
        for pattern, parser in self.action_patterns:
            matches = re.finditer(pattern, cleaned_text)
            
            for match in matches:
                try:
                    action = parser(match)
                    actions.append(action)
                    
                    # Remove the action from the text
                    cleaned_text = cleaned_text.replace(match.group(0), "")
                except Exception as e:
                    logger.warning(f"Failed to parse action: {match.group(0)}, error: {e}")
        
        # Clean up the text
        cleaned_text = self._clean_text(cleaned_text)
        
        return cleaned_text, actions
    
    def _clean_text(self, text: str) -> str:
        """
        Clean up text by removing extra whitespace and normalizing line breaks.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        # Replace multiple newlines with a single newline
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Replace multiple spaces with a single space
        text = re.sub(r' {2,}', ' ', text)
        
        # Trim whitespace
        text = text.strip()
        
        return text
