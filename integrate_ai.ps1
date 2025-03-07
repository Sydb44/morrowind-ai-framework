# Morrowind AI Framework - Integration Script
$ErrorActionPreference = "Stop"

$BASE_DIR = "f:/Projects/morrowind_ai_framework"
$OPENMW_DIR = "$BASE_DIR/openmw-source"
$CLIENT_DIR = "$BASE_DIR/openmw-client"

Write-Host "Copying AI components to OpenMW source tree..."
New-Item -ItemType Directory -Force -Path "$OPENMW_DIR/components/ai_client" | Out-Null
Copy-Item -Force -Recurse "$CLIENT_DIR/components/ai_client/*" "$OPENMW_DIR/components/ai_client/"

New-Item -ItemType Directory -Force -Path "$OPENMW_DIR/components/openmw-mp/mwbase" | Out-Null
Copy-Item -Force -Recurse "$CLIENT_DIR/components/openmw-mp/*" "$OPENMW_DIR/components/openmw-mp/"

Write-Host "`nCopying Lua scripts to OpenMW resources..."
New-Item -ItemType Directory -Force -Path "$OPENMW_DIR/resources/lua" | Out-Null
Copy-Item -Force -Recurse "$CLIENT_DIR/resources/lua/*" "$OPENMW_DIR/resources/lua/"

Write-Host "`nUpdating CMake configuration..."
$cmakeContent = Get-Content "$OPENMW_DIR/components/CMakeLists.txt"
if (-not ($cmakeContent -match "add_component_dir\(ai_client client\)")) {
    Add-Content "$OPENMW_DIR/components/CMakeLists.txt" "`nadd_component_dir(ai_client client)"
}

Write-Host "`nCreating build directory..."
New-Item -ItemType Directory -Force -Path "$OPENMW_DIR/build" | Out-Null

Write-Host "`nCreating AI configuration for OpenMW..."
@"
# AI Framework Configuration
enable lua = true
lua ai_npc_dialogue.lua
ai server host = localhost
ai server port = 8082
"@ | Set-Content "$OPENMW_DIR/build/ai_config.cfg"

Write-Host "`nModifying OpenMW engine files..."

# Add include to engine.cpp
$engineCpp = Get-Content "$OPENMW_DIR/apps/openmw/engine.cpp"
$includeIndex = $engineCpp | Select-String -Pattern "#include <components/misc/stringops.hpp>" | Select-Object -ExpandProperty LineNumber
$engineCpp = $engineCpp[0..($includeIndex-1)] + 
    "#include <components/openmw-mp/mwbase/aimanagerimpl.hpp>" +
    $engineCpp[$includeIndex..($engineCpp.Length-1)]

# Add AI Manager initialization
$stateManagerIndex = $engineCpp | Select-String -Pattern "mStateManager = std::make_unique<MWState::StateManager>" | Select-Object -ExpandProperty LineNumber
$aiManagerInit = @"

    // AI Manager
    std::string aiServerHost = mCfgMgr.getStringOption("ai server host", "localhost");
    int aiServerPort = mCfgMgr.getIntOption("ai server port", 8080);
    
    mAIManager = new MWBase::AIManagerImpl();
    mAIManager->init(aiServerHost, aiServerPort);
    mEnvironment.setAIManager(mAIManager);

"@
$engineCpp = $engineCpp[0..($stateManagerIndex)] + $aiManagerInit + $engineCpp[($stateManagerIndex+1)..($engineCpp.Length-1)]
$engineCpp | Set-Content "$OPENMW_DIR/apps/openmw/engine.cpp"

Write-Host "`nIntegration completed!"
Write-Host "`nNext steps:"
Write-Host "1. Configure and build OpenMW:"
Write-Host "   cd $OPENMW_DIR/build"
Write-Host "   cmake .."
Write-Host "   cmake --build . --config Release"
Write-Host "`n2. Start the AI server:"
Write-Host "   $BASE_DIR/ai-server/start_server.bat"
Write-Host "`n3. Launch OpenMW with the AI integration"
Write-Host "`n4. Test with an NPC that has the AIDialogue script"
