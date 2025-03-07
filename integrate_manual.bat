@echo off
REM Morrowind AI Framework - Manual Integration Script

echo Creating backup of original files...
mkdir "f:/Projects/morrowind_ai_framework/openmw-source/backup"
copy "f:/Projects/morrowind_ai_framework/openmw-source/apps/openmw/engine.cpp" "f:/Projects/morrowind_ai_framework/openmw-source/backup/engine.cpp.bak"
copy "f:/Projects/morrowind_ai_framework/openmw-source/apps/openmw/engine.hpp" "f:/Projects/morrowind_ai_framework/openmw-source/backup/engine.hpp.bak"
copy "f:/Projects/morrowind_ai_framework/openmw-source/apps/openmw/mwbase/environment.cpp" "f:/Projects/morrowind_ai_framework/openmw-source/backup/environment.cpp.bak"
copy "f:/Projects/morrowind_ai_framework/openmw-source/apps/openmw/mwbase/environment.hpp" "f:/Projects/morrowind_ai_framework/openmw-source/backup/environment.hpp.bak"
copy "f:/Projects/morrowind_ai_framework/openmw-source/components/CMakeLists.txt" "f:/Projects/morrowind_ai_framework/openmw-source/backup/CMakeLists.txt.bak"

echo.
echo Copying AI components to OpenMW source tree...
mkdir "f:/Projects/morrowind_ai_framework/openmw-source/components/ai_client"
xcopy /E /Y "f:/Projects/morrowind_ai_framework/openmw-client/components/ai_client\*" "f:/Projects/morrowind_ai_framework/openmw-source/components/ai_client\"

mkdir "f:/Projects/morrowind_ai_framework/openmw-source/components/openmw-mp/mwbase"
xcopy /E /Y "f:/Projects/morrowind_ai_framework/openmw-client/components/openmw-mp\*" "f:/Projects/morrowind_ai_framework/openmw-source/components/openmw-mp\"

echo.
echo Copying Lua scripts to OpenMW resources...
mkdir "f:/Projects/morrowind_ai_framework/openmw-source/resources/lua"
xcopy /E /Y "f:/Projects/morrowind_ai_framework/openmw-client/resources/lua\*" "f:/Projects/morrowind_ai_framework/openmw-source/resources/lua\"

echo.
echo Updating CMake configuration...
echo add_component_dir(ai_client client) >> "f:/Projects/morrowind_ai_framework/openmw-source/components/CMakeLists.txt"

echo.
echo Creating build directory...
mkdir "f:/Projects/morrowind_ai_framework/openmw-source/build"

echo.
echo Creating AI configuration for OpenMW...
echo # AI Framework Configuration > "f:/Projects/morrowind_ai_framework/openmw-source/build/ai_config.cfg"
echo enable lua = true >> "f:/Projects/morrowind_ai_framework/openmw-source/build/ai_config.cfg"
echo lua ai_npc_dialogue.lua >> "f:/Projects/morrowind_ai_framework/openmw-source/build/ai_config.cfg"
echo ai server host = localhost >> "f:/Projects/morrowind_ai_framework/openmw-source/build/ai_config.cfg"
echo ai server port = 8082 >> "f:/Projects/morrowind_ai_framework/openmw-source/build/ai_config.cfg"

echo.
echo Applying changes to OpenMW engine files...

REM Modify engine.hpp
echo Adding AIManager to engine.hpp...
echo class AIManager; >> "f:/Projects/morrowind_ai_framework/openmw-source/apps/openmw/mwbase/aimanager.hpp"
echo MWBase::AIManager* mAIManager; >> "f:/Projects/morrowind_ai_framework/openmw-source/apps/openmw/engine.hpp"

REM Modify engine.cpp
echo Adding AIManager initialization to engine.cpp...
echo #include ^<components/openmw-mp/mwbase/aimanagerimpl.hpp^> >> "f:/Projects/morrowind_ai_framework/openmw-source/apps/openmw/engine.cpp"
echo mAIManager = new MWBase::AIManagerImpl(); >> "f:/Projects/morrowind_ai_framework/openmw-source/apps/openmw/engine.cpp"
echo mAIManager-^>init(aiServerHost, aiServerPort); >> "f:/Projects/morrowind_ai_framework/openmw-source/apps/openmw/engine.cpp"
echo mEnvironment.setAIManager(mAIManager); >> "f:/Projects/morrowind_ai_framework/openmw-source/apps/openmw/engine.cpp"

REM Modify environment files
echo Adding AIManager to environment...
echo AIManager* mAIManager; >> "f:/Projects/morrowind_ai_framework/openmw-source/apps/openmw/mwbase/environment.hpp"
echo void Environment::setAIManager(AIManager* manager) { mAIManager = manager; } >> "f:/Projects/morrowind_ai_framework/openmw-source/apps/openmw/mwbase/environment.cpp"

echo.
echo Integration completed!
echo.
echo Next steps:
echo 1. Start the AI server: f:/Projects/morrowind_ai_framework/ai-server/start_server.bat
echo 2. Launch OpenMW with the AI integration
echo 3. Test with an NPC that has the AIDialogue script

echo.
echo Press any key to exit...
pause >nul
