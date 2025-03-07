# Morrowind AI Framework - AI Server

This is the AI server component of the Morrowind AI Framework, which provides intelligent NPC dialogue and behavior for the game Morrowind using OpenMW.

## Overview

The AI server is a WebSocket server that receives requests from the OpenMW client and generates responses using large language models (LLMs). It supports:

- Dynamic dialogue generation based on NPC personality, background, and context
- Memory persistence for NPCs to remember past interactions
- Action parsing to extract game actions from LLM responses
- Voice generation for NPC dialogue (optional)
- Multiple LLM providers (OpenAI, Anthropic, local models)

## Requirements

- Python 3.9 or later
- Dependencies listed in `requirements.txt`
- API keys for LLM providers:
  - OpenAI API key (version 0.28.0 required)
  - Anthropic API key (optional)
  - ElevenLabs API key (optional, for voice generation)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/example/morrowind-ai-framework.git
   cd morrowind_ai_framework/ai-server
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Copy the example configuration files:
   ```bash
   cp config.json.example config.json
   cp .env.example .env
   ```

6. Edit the configuration files to match your setup:
   - `config.json`: Server configuration
   - `.env`: API keys and environment variables

## Configuration

### Server Configuration (config.json)

```json
{
  "server": {
    "host": "localhost",
    "port": 8082,
    "max_connections": 100,
    "connection_timeout": 30
  },
  "llm": {
    "provider": "openai",
    "model": "gpt-4",
    "api_version": "0.28.0",
    "temperature": 0.7,
    "max_tokens": 150,
    "frequency_penalty": 0.3,
    "presence_penalty": 0.3
  },
  "memory": {
    "max_history": 50,
    "persistence_dir": "memories",
    "save_interval": 300
  },
  "voice": {
    "enabled": false,
    "provider": "elevenlabs",
    "output_dir": "voice-output",
    "cache_size": 1000
  },
  "logging": {
    "level": "INFO",
    "file": "logs/server.log",
    "max_size": 10485760,
    "backup_count": 5
  }
}
```

### Environment Variables (.env)

```ini
# OpenAI Configuration (Required)
OPENAI_API_KEY=your_api_key_here
OPENAI_API_VERSION=0.28.0  # Required version for compatibility

# Anthropic Configuration (Optional)
ANTHROPIC_API_KEY=your_api_key_here

# ElevenLabs Configuration (Optional)
ELEVENLABS_API_KEY=your_api_key_here

# Server Security (Optional)
AUTH_TOKEN=your_auth_token_here
```

## Usage

### Starting the Server

You can start the server using the provided scripts:

- Windows: `start_server.bat`
- Unix/MacOS: `./start_server.sh`

Or manually:

```bash
python run_server.py
```

The server will start on the host and port specified in your configuration (default: `localhost:8082`).

### Testing the Server

You can test the server using the provided test script:

```bash
python test_server.py
```

Or using the example client:

```bash
python example_client.py
```

For interactive testing, use:

```bash
python example_client.py --interactive
```

## Directory Structure

- `src/`: Source code for the AI server
  - `server.py`: Main server implementation
  - `config.py`: Configuration handling
  - `context_manager.py`: NPC context and memory management
  - `llm_interface.py`: Interface for LLM providers
  - `prompt_manager.py`: Prompt generation and management
  - `action_parser.py`: Action parsing from LLM responses
  - `voice_system.py`: Voice generation
- `static-data/`: Static data for the AI server
  - `factions.json`: Information about factions
  - `locations.json`: Information about locations
  - `lore.json`: General lore information
  - `templates/`: Prompt templates
- `npc-profiles/`: NPC profiles
- `memories/`: NPC memories (generated)
- `logs/`: Server logs (generated)
- `voice-output/`: Generated voice files (generated)
- `conversation-logs/`: Conversation logs (generated)

## Memory Management

The server manages NPC memories through JSON files stored in the `memories/` directory:

```json
{
  "npc_id": "example_npc",
  "conversations": [
    {
      "timestamp": "2025-03-06T23:55:14",
      "player_text": "Hello there",
      "response": "Greetings, outlander",
      "context": {
        "location": "Balmora",
        "time_of_day": "evening",
        "player_faction": "none"
      }
    }
  ],
  "relationships": {
    "player": {
      "disposition": 50,
      "interactions": 1,
      "last_interaction": "2025-03-06T23:55:14"
    }
  },
  "knowledge": {
    "player_name": "Unknown",
    "player_class": "Unknown",
    "shared_information": []
  }
}
```

## Performance Optimization

1. **Memory Usage**
   - Set appropriate `max_history` in config.json
   - Enable periodic memory cleanup
   - Monitor memory directory size

2. **Response Latency**
   - Use connection pooling
   - Enable response caching
   - Optimize prompt length

3. **Voice Generation**
   - Enable voice caching
   - Set appropriate cache size
   - Monitor voice-output directory

## Troubleshooting

### Common Issues

1. **OpenAI API Version**
   - Error: "API version not compatible"
   - Solution: Pin to version 0.28.0 in .env
   - Future: Monitor for API updates

2. **Memory Persistence**
   - Issue: Growing memory files
   - Solution: Configure cleanup in config.json
   - Monitor: Check logs/memory_usage.log

3. **Voice Generation**
   - Error: Voice API rate limits
   - Solution: Enable caching
   - Alternative: Disable voice features

### Logging

The server maintains several log files:

- `server.log`: Main server operations
- `memory_usage.log`: Memory management
- `api_calls.log`: LLM API interactions
- `voice_gen.log`: Voice generation

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
