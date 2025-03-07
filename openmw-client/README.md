# Morrowind AI Framework - OpenMW Client Integration

This is the OpenMW client integration component of the Morrowind AI Framework, which connects the OpenMW engine with the AI server to provide intelligent NPC dialogue and behavior.

## Overview

The OpenMW client integration consists of C++ components and Lua scripts that enable communication between the OpenMW engine and the AI server. It handles:

- WebSocket communication with the AI server
- Integration with OpenMW's dialogue system
- Event handling for game events
- Action execution for NPC behaviors
- Memory persistence for NPC interactions

## Requirements

- OpenMW 0.49.0 (required for latest integration features)
- C++ compiler with C++17 support
- CMake 3.12 or later
- Boost libraries (for WebSocket client)
- Lua 5.1 or later (included with OpenMW)

## Installation

### Building from Source

1. Clone the OpenMW repository:
   ```bash
   git clone https://github.com/OpenMW/openmw.git
   cd openmw
   git checkout openmw-0.49.0
   ```

2. Choose an integration method:

   a. Using the automated script (recommended):
   ```bash
   # Windows
   integrate_with_openmw.bat

   # Linux/macOS
   chmod +x integrate_with_openmw.sh
   ./integrate_with_openmw.sh
   ```

   b. Using the manual integration script (for custom setups):
   ```bash
   # Windows
   integrate_manual_v3.bat  # Latest version with improved error handling

   # Linux/macOS
   # Follow manual integration steps below
   ```

   c. Manual integration steps:
   ```bash
   # 1. Copy AI components
   cp -r /path/to/morrowind_ai_framework/openmw-client/components/* components/

   # 2. Copy Lua scripts
   cp -r /path/to/morrowind_ai_framework/openmw-client/resources/lua resources/

   # 3. Apply the patch
   git apply /path/to/morrowind_ai_framework/openmw-source/apps/openmw/engine.cpp.patch

   # 4. Update CMake configuration
   echo "add_component_dir(ai_client client)" >> components/CMakeLists.txt
   ```

3. Build OpenMW:
   ```bash
   mkdir build
   cd build
   cmake ..
   cmake --build . --config Release  # Windows
   make -j$(nproc)                  # Linux/macOS
   ```

## Configuration

### OpenMW Configuration

Add to your `openmw.cfg`:

```ini
# Enable Lua scripting
enable lua = true

# Load AI Framework Lua scripts
lua ai_npc_dialogue.lua

# AI Server connection settings (must match server config)
ai server host = localhost
ai server port = 8082  # Default port, ensure it matches AI server configuration
```

### NPC Configuration

To enable AI dialogue for an NPC:

1. Create an NPC profile in the AI server's `npc-profiles` directory
2. Add the AIDialogue script to the NPC:
   ```
   Begin AIDialogue
       NPCId "your_npc_id"  # Must match profile name in AI server
   End
   ```

## Components

### C++ Components

- `ai_client/`: WebSocket client and core AI integration
  - `client.hpp/cpp`: Main WebSocket client implementation
  - `CMakeLists.txt`: Build configuration

- `openmw-mp/mwbase/`: AI Manager interface and implementation
  - `aimanager.hpp`: Core AI manager interface
  - `aimanagerimpl.hpp/cpp`: Implementation of AI manager

- `lua/`: Lua bindings and scripting support
  - `ai.hpp/cpp`: Lua bindings for AI system

### Lua Scripts

- `ai_npc_dialogue.lua`: Main NPC dialogue handling script
  - Manages dialogue flow
  - Handles NPC responses
  - Processes game events
  - Executes NPC actions

## Memory Management

The AI Framework maintains persistent memory for NPCs through:
- Conversation history storage
- Event memory tracking
- Relationship status persistence
- Action history logging

Memory files are stored in the AI server's `memories` directory and are automatically managed.

## Performance Considerations

- WebSocket connections are pooled and reused
- NPC contexts are cached to reduce latency
- Memory usage is monitored and optimized
- Long-running operations are handled asynchronously

## Troubleshooting

### Common Issues

1. **Integration Failures**
   - Verify OpenMW version is exactly 0.49.0
   - Check all required dependencies are installed
   - Ensure patch hasn't been previously applied
   - Try using integrate_manual_v3.bat for better error reporting

2. **Build Errors**
   - Confirm C++17 compiler is available
   - Verify Boost libraries are correctly installed
   - Check CMake version is 3.12 or later
   - Review build logs for specific errors

3. **Runtime Issues**
   - Verify AI server is running and accessible
   - Check port configuration matches between client and server
   - Ensure Lua scripts are correctly installed
   - Monitor OpenMW logs for error messages

4. **NPC Dialogue Problems**
   - Confirm NPC profile exists and ID matches
   - Check AI server logs for response errors
   - Verify WebSocket connection is established
   - Test with example_npc profile first

### Logs and Debugging

Important log locations:
- OpenMW logs: `openmw.log`
- AI server logs: `ai-server/logs/`
- NPC memory files: `ai-server/memories/`
- Conversation logs: `ai-server/conversation-logs/`

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
