# Morrowind AI Framework - OpenMW Integration Guide

This guide provides comprehensive instructions for integrating the Morrowind AI Framework with OpenMW 0.49.0. The integration enables NPCs to generate dynamic, contextually aware dialogue using the AI server.

## Prerequisites

- OpenMW 0.49.0 source code
- C++ compiler with C++17 support
- CMake 3.12 or later
- Boost libraries (for WebSocket client)
- Git (for version control)
- Visual Studio 2022 (for Windows builds)
- Qt 5.15.2 (for Windows builds)

## Integration Methods

We provide several integration methods to accommodate different needs and environments:

### 1. Automated Integration (Recommended)

The standard automated integration script that works for most setups:

#### Windows
```bash
integrate_with_openmw.bat
```
- Automatically detects OpenMW source directory
- Creates integration branch
- Applies all necessary patches
- Configures CMake
- Builds OpenMW

#### Linux/macOS
```bash
chmod +x integrate_with_openmw.sh
./integrate_with_openmw.sh
```
- Similar functionality to Windows version
- Handles platform-specific paths and commands

### 2. Fixed Path Integration

For systems with specific directory structures:

```bash
integrate_with_openmw_fixed.bat
```
- Uses predefined paths (f:/Projects/morrowind_ai_framework)
- Skips path detection and prompts
- Useful for automated builds or known environments

### 3. Manual Integration with Error Handling

A series of scripts with increasing levels of error handling and features:

#### integrate_manual.bat
- Basic integration script
- Minimal error handling
- Creates backups of modified files

#### integrate_manual_v2.bat
- Improved error checking
- Better path handling
- Verifies file existence before operations

#### integrate_manual_v3.bat (Latest)
- Comprehensive error handling
- Detailed progress reporting
- Recovery options for failed operations
- Best choice for troubleshooting integration issues

### 4. PowerShell Integration

For advanced Windows users:

```powershell
integrate_ai.ps1
```
- PowerShell-native implementation
- Advanced error handling
- Detailed logging
- Support for Windows security features

## Integration Process Details

The integration process involves several key steps:

### 1. Source Code Preparation

```bash
# Clone OpenMW
git clone https://github.com/OpenMW/openmw.git
cd openmw
git checkout openmw-0.49.0

# Create integration branch
git checkout -b morrowind-ai-integration
```

### 2. Component Installation

```bash
# Copy AI components
cp -r /path/to/morrowind_ai_framework/openmw-client/components/* components/

# Copy Lua scripts
cp -r /path/to/morrowind_ai_framework/openmw-client/resources/lua resources/
```

### 3. Engine Modifications

```bash
# Apply the patch
git apply /path/to/morrowind_ai_framework/openmw-source/apps/openmw/engine.cpp.patch

# Update CMake configuration
echo "add_component_dir(ai_client client)" >> components/CMakeLists.txt
```

### 4. Build Configuration

```bash
mkdir build
cd build
cmake ..
cmake --build . --config Release  # Windows
make -j$(nproc)                  # Linux/macOS
```

### 5. OpenMW Configuration

Add to `openmw.cfg`:
```ini
enable lua = true
lua ai_npc_dialogue.lua
ai server host = localhost
ai server port = 8082
```

## Troubleshooting

### Common Issues and Solutions

1. **CMake Configuration Fails**
   - Verify Qt installation (Windows)
   - Check Boost libraries
   - Ensure vcpkg is properly configured
   - Use integrate_manual_v3.bat for detailed error messages

2. **Patch Application Fails**
   - Check OpenMW version (must be 0.49.0)
   - Verify patch hasn't been applied already
   - Use manual patch application:
     ```bash
     patch -p1 < engine.cpp.patch
     ```

3. **Build Errors**
   - Check compiler version
   - Verify all dependencies
   - Review CMake output
   - Check build logs

4. **Runtime Issues**
   - Verify AI server is running
   - Check port configuration
   - Review OpenMW logs
   - Test with example NPC

### Integration Script Selection Guide

Choose the appropriate integration script based on your needs:

1. **Standard Setup**
   - Use `integrate_with_openmw.bat`/`.sh`
   - Best for most users
   - Automated process

2. **Known Environment**
   - Use `integrate_with_openmw_fixed.bat`
   - Fixed paths
   - Faster integration

3. **Troubleshooting**
   - Use `integrate_manual_v3.bat`
   - Detailed error reporting
   - Step-by-step verification

4. **Advanced Windows Users**
   - Use `integrate_ai.ps1`
   - PowerShell features
   - Enhanced logging

## Reverting Integration

If you need to revert the integration:

1. Restore backups:
   ```bash
   cd openmw-source/backup
   cp * ../
   ```

2. Or use Git:
   ```bash
   git checkout openmw-0.49.0
   git clean -fd
   ```

3. Rebuild OpenMW:
   ```bash
   cd build
   cmake ..
   cmake --build . --config Release
   ```

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the integration logs
3. Use integrate_manual_v3.bat for detailed error reporting
4. Check the OpenMW forums
5. Report issues on the project repository

## License

This integration guide and associated scripts are licensed under the MIT License - see the LICENSE file for details.
