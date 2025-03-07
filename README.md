# Morrowind AI Framework

The Morrowind AI Framework is a comprehensive system that enhances NPC interactions in The Elder Scrolls III: Morrowind by integrating large language models (LLMs) to generate dynamic, contextually aware dialogue and behaviors.

## Overview

This framework consists of two main components:

1. **AI Server**: A Python-based WebSocket server that processes dialogue requests using LLMs and generates appropriate responses based on NPC personality, game context, and conversation history.

2. **OpenMW Client Integration**: C++ components and Lua scripts that integrate with the OpenMW engine to connect in-game NPCs with the AI server.

The framework enables NPCs to:
- Generate dynamic, contextually relevant dialogue
- Remember past interactions with the player
- Respond appropriately to game events
- Perform in-game actions based on conversation
- Optionally speak with synthesized voices

## Features

- **Dynamic Dialogue**: NPCs generate unique, contextually appropriate responses rather than using pre-written dialogue.
- **Memory Persistence**: NPCs remember past interactions with the player and important events.
- **Action Integration**: NPCs can perform game actions like giving items, starting combat, or initiating barter.
- **Voice Generation**: Optional text-to-speech integration for voiced dialogue.
- **Multiple LLM Support**: Compatible with various LLM providers:
  - OpenAI (API version 0.28.0 required for compatibility)
  - Anthropic
  - Local models
- **Lore Consistency**: Built-in knowledge of Morrowind lore, factions, locations, and characters.
- **Extensible Architecture**: Easy to add new NPCs, locations, and lore.

## Prerequisites

- OpenMW 0.49.0 (required for latest integration features)
- Python 3.9 or later
- C++ compiler with C++17 support
- CMake 3.12 or later
- Boost libraries (for WebSocket client)
- API keys for chosen LLM provider(s)

## Installation

### AI Server Setup

1. Navigate to the AI server directory:
   ```bash
   cd morrowind_ai_framework/ai-server
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Unix/MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the server:
   ```bash
   cp config.json.example config.json
   cp .env.example .env
   ```
   Edit these files to add your API keys and customize settings.

### OpenMW Integration

We provide several integration methods to suit different needs:

#### 1. Automated Integration (Recommended)

```bash
# Windows
cd morrowind_ai_framework
integrate_with_openmw.bat

# Linux/macOS
cd morrowind_ai_framework
chmod +x integrate_with_openmw.sh
./integrate_with_openmw.sh
```

#### 2. Manual Integration with Error Handling

For custom setups or when troubleshooting is needed:

```bash
# Windows
integrate_manual_v3.bat  # Latest version with improved error handling

# Linux/macOS
# Follow manual integration steps in INTEGRATION_README.md
```

#### 3. Fixed Path Integration

For systems with specific directory structures:

```bash
integrate_with_openmw_fixed.bat
```

For detailed instructions and manual integration steps, see the [Integration README](INTEGRATION_README.md).

## Usage

1. Start the AI server:
   ```bash
   cd morrowind_ai_framework/ai-server
   # Windows
   start_server.bat
   # Linux/macOS
   ./start_server.sh
   ```

2. Launch OpenMW with the AI integration enabled.

3. Interact with NPCs in the game to experience dynamic dialogue.

## Testing

To verify the integration:

1. Start the AI server
2. Launch OpenMW with the AI Framework enabled
3. Run the test script:
   ```lua
   runlua "f:/Projects/morrowind_ai_framework/test_ai_integration.lua"
   ```

This creates a test NPC and initiates dialogue to verify the integration.

## Configuration

### AI Server Configuration

Edit `ai-server/config.json` to configure:
- LLM provider settings
- Voice generation options
- WebSocket server settings
- Memory management
- Logging preferences

### OpenMW Configuration

Add to your `openmw.cfg`:
```ini
enable lua = true
lua ai_npc_dialogue.lua
ai server host = localhost
ai server port = 8082
```

## Adding New NPCs

1. Create a JSON profile in `ai-server/npc-profiles/`:
   ```json
   {
     "id": "your_npc_id",
     "name": "NPC Name",
     "personality": "Brief personality description",
     "background": "Character background",
     "faction": "Optional faction affiliation",
     "location": "Current location"
   }
   ```

2. Add the AIDialogue script to the NPC:
   ```
   Begin AIDialogue
       NPCId "your_npc_id"
   End
   ```

## Known Issues

1. **OpenAI API Compatibility**
   - Version 0.28.0 required due to breaking changes in newer versions
   - Future updates will address newer API versions

2. **Integration Complexity**
   - Core OpenMW file modifications required
   - Multiple integration scripts available for different scenarios
   - Use integrate_manual_v3.bat for best error handling

3. **Performance**
   - Dialogue generation latency varies by LLM provider
   - Memory usage increases with NPC conversation history
   - WebSocket connection pooling recommended for multiple NPCs

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The OpenMW team for their incredible work on the open-source Morrowind engine
- The developers of the language models that power the dialogue generation
- The Morrowind modding community for their inspiration and support
