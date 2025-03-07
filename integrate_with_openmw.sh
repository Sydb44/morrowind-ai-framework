#!/bin/bash
# Morrowind AI Framework - OpenMW Integration Script
# This script automates the integration of the Morrowind AI Framework with OpenMW

echo "Morrowind AI Framework - OpenMW Integration Script"
echo "==================================================="

# Set paths
FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENMW_DIR=""
OPENMW_BUILD_DIR=""

# Ask for OpenMW source directory
echo
echo "Please enter the path to your OpenMW source directory:"
read -r OPENMW_DIR

# Validate OpenMW directory
if [ ! -f "$OPENMW_DIR/CMakeLists.txt" ]; then
    echo "Error: Invalid OpenMW directory. CMakeLists.txt not found."
    exit 1
fi

# Check OpenMW version
echo
echo "Checking OpenMW version..."
if ! grep -q "Version: 0.49.0" "$OPENMW_DIR/README.md"; then
    echo "Warning: This integration is designed for OpenMW 0.49.0."
    echo "Current version may be different. Continue at your own risk."
    echo
    echo "Do you want to continue? (y/n)"
    read -r CONTINUE
    if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
        exit 1
    fi
fi

# Create backup
echo
echo "Creating backup of original files..."
mkdir -p "$OPENMW_DIR/backup"
cp "$OPENMW_DIR/apps/openmw/engine.cpp" "$OPENMW_DIR/backup/engine.cpp.bak"
cp "$OPENMW_DIR/apps/openmw/engine.hpp" "$OPENMW_DIR/backup/engine.hpp.bak"
cp "$OPENMW_DIR/apps/openmw/mwbase/environment.cpp" "$OPENMW_DIR/backup/environment.cpp.bak"
cp "$OPENMW_DIR/apps/openmw/mwbase/environment.hpp" "$OPENMW_DIR/backup/environment.hpp.bak"
cp "$OPENMW_DIR/components/CMakeLists.txt" "$OPENMW_DIR/backup/CMakeLists.txt.bak"

# Create integration branch
echo
echo "Creating integration branch..."
cd "$OPENMW_DIR" || exit 1
git checkout -b morrowind-ai-integration

# Copy AI components
echo
echo "Copying AI components to OpenMW source tree..."
mkdir -p "$OPENMW_DIR/components/ai_client"
cp -r "$FRAMEWORK_DIR/openmw-client/components/ai_client/"* "$OPENMW_DIR/components/ai_client/"

mkdir -p "$OPENMW_DIR/components/openmw-mp/mwbase"
cp -r "$FRAMEWORK_DIR/openmw-client/components/openmw-mp/"* "$OPENMW_DIR/components/openmw-mp/"

# Copy Lua scripts
echo
echo "Copying Lua scripts to OpenMW resources..."
mkdir -p "$OPENMW_DIR/resources/lua"
cp -r "$FRAMEWORK_DIR/openmw-client/resources/lua/"* "$OPENMW_DIR/resources/lua/"

# Apply patch
echo
echo "Applying patch to OpenMW engine..."
cd "$OPENMW_DIR" || exit 1
git apply "$FRAMEWORK_DIR/openmw-source/apps/openmw/engine.cpp.patch"
if [ $? -ne 0 ]; then
    echo "Error: Failed to apply patch. Please check if the patch is compatible with your OpenMW version."
    exit 1
fi

# Update CMakeLists.txt
echo
echo "Updating CMake configuration..."
echo "add_component_dir(ai_client client)" >> "$OPENMW_DIR/components/CMakeLists.txt"

# Create build directory
echo
echo "Setting up build directory..."
mkdir -p "$OPENMW_DIR/build"
OPENMW_BUILD_DIR="$OPENMW_DIR/build"

# Configure and build
echo
echo "Do you want to configure and build OpenMW now? (y/n)"
read -r BUILD
if [ "$BUILD" = "y" ] || [ "$BUILD" = "Y" ]; then
    echo
    echo "Configuring build..."
    cd "$OPENMW_BUILD_DIR" || exit 1
    cmake ..
    
    echo
    echo "Building OpenMW..."
    make -j"$(nproc)"
fi

# Create configuration file
echo
echo "Creating AI configuration for OpenMW..."
cat > "$OPENMW_BUILD_DIR/ai_config.cfg" << EOF
# AI Framework Configuration
enable lua = true
lua ai_npc_dialogue.lua
ai server host = localhost
ai server port = 8082
EOF

echo
echo "Add the contents of ai_config.cfg to your openmw.cfg file."

echo
echo "Integration completed successfully!"
echo
echo "Next steps:"
echo "1. Start the AI server: $FRAMEWORK_DIR/ai-server/start_server.sh"
echo "2. Launch OpenMW with the AI integration"
echo "3. Test with an NPC that has the AIDialogue script"

echo
echo "Press any key to exit..."
read -n 1
