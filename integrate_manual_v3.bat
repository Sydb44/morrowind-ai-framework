@echo off
REM Morrowind AI Framework - Manual Integration Script

set BASE_DIR=f:/Projects/morrowind_ai_framework
set OPENMW_DIR=%BASE_DIR%/openmw-source
set CLIENT_DIR=%BASE_DIR%/openmw-client

echo Copying AI components to OpenMW source tree...
if not exist "%OPENMW_DIR%\components\ai_client" mkdir "%OPENMW_DIR%\components\ai_client"
xcopy /E /Y /I "%CLIENT_DIR%\components\ai_client\*" "%OPENMW_DIR%\components\ai_client\"

if not exist "%OPENMW_DIR%\components\openmw-mp\mwbase" mkdir "%OPENMW_DIR%\components\openmw-mp\mwbase"
xcopy /E /Y /I "%CLIENT_DIR%\components\openmw-mp\*" "%OPENMW_DIR%\components\openmw-mp\"

echo.
echo Copying Lua scripts to OpenMW resources...
if not exist "%OPENMW_DIR%\resources\lua" mkdir "%OPENMW_DIR%\resources\lua"
xcopy /E /Y /I "%CLIENT_DIR%\resources\lua\*" "%OPENMW_DIR%\resources\lua\"

echo.
echo Updating CMake configuration...
findstr /i /c:"add_component_dir(ai_client client)" "%OPENMW_DIR%\components\CMakeLists.txt" > nul
if errorlevel 1 (
    echo add_component_dir(ai_client client) >> "%OPENMW_DIR%\components\CMakeLists.txt"
)

echo.
echo Creating build directory...
if not exist "%OPENMW_DIR%\build" mkdir "%OPENMW_DIR%\build"

echo.
echo Creating AI configuration for OpenMW...
echo # AI Framework Configuration > "%OPENMW_DIR%\build\ai_config.cfg"
echo enable lua = true >> "%OPENMW_DIR%\build\ai_config.cfg"
echo lua ai_npc_dialogue.lua >> "%OPENMW_DIR%\build\ai_config.cfg"
echo ai server host = localhost >> "%OPENMW_DIR%\build\ai_config.cfg"
echo ai server port = 8082 >> "%OPENMW_DIR%\build\ai_config.cfg"

echo.
echo Creating temporary files for modifications...

REM Create AIManager header
echo namespace MWBase { > "%OPENMW_DIR%\apps\openmw\mwbase\aimanager.hpp.new"
echo class AIManager { >> "%OPENMW_DIR%\apps\openmw\mwbase\aimanager.hpp.new"
echo public: >> "%OPENMW_DIR%\apps\openmw\mwbase\aimanager.hpp.new"
echo     virtual ~AIManager() {} >> "%OPENMW_DIR%\apps\openmw\mwbase\aimanager.hpp.new"
echo     virtual void init(const std::string& host, int port) = 0; >> "%OPENMW_DIR%\apps\openmw\mwbase\aimanager.hpp.new"
echo }; >> "%OPENMW_DIR%\apps\openmw\mwbase\aimanager.hpp.new"
echo } >> "%OPENMW_DIR%\apps\openmw\mwbase\aimanager.hpp.new"
move /Y "%OPENMW_DIR%\apps\openmw\mwbase\aimanager.hpp.new" "%OPENMW_DIR%\apps\openmw\mwbase\aimanager.hpp"

REM Add AIManager to environment.hpp
echo class AIManager; >> "%OPENMW_DIR%\apps\openmw\mwbase\environment.hpp"
echo AIManager* mAIManager; >> "%OPENMW_DIR%\apps\openmw\mwbase\environment.hpp"
echo void setAIManager(AIManager* manager); >> "%OPENMW_DIR%\apps\openmw\mwbase\environment.hpp"

REM Add AIManager implementation to environment.cpp
echo void Environment::setAIManager(AIManager* manager) { mAIManager = manager; } >> "%OPENMW_DIR%\apps\openmw\mwbase\environment.cpp"

REM Add AIManager to engine.hpp
echo #include "mwbase/aimanager.hpp" >> "%OPENMW_DIR%\apps\openmw\engine.hpp"
echo MWBase::AIManager* mAIManager; >> "%OPENMW_DIR%\apps\openmw\engine.hpp"

REM Add AIManager initialization to engine.cpp
echo #include ^<components/openmw-mp/mwbase/aimanagerimpl.hpp^> >> "%OPENMW_DIR%\apps\openmw\engine.cpp"
echo // AI Manager >> "%OPENMW_DIR%\apps\openmw\engine.cpp"
echo std::string aiServerHost = mCfgMgr.getStringOption("ai server host", "localhost"); >> "%OPENMW_DIR%\apps\openmw\engine.cpp"
echo int aiServerPort = mCfgMgr.getIntOption("ai server port", 8080); >> "%OPENMW_DIR%\apps\openmw\engine.cpp"
echo mAIManager = new MWBase::AIManagerImpl(); >> "%OPENMW_DIR%\apps\openmw\engine.cpp"
echo mAIManager-^>init(aiServerHost, aiServerPort); >> "%OPENMW_DIR%\apps\openmw\engine.cpp"
echo mEnvironment.setAIManager(mAIManager); >> "%OPENMW_DIR%\apps\openmw\engine.cpp"

echo.
echo Integration completed!
echo.
echo Next steps:
echo 1. Start the AI server: %BASE_DIR%\ai-server\start_server.bat
echo 2. Launch OpenMW with the AI integration
echo 3. Test with an NPC that has the AIDialogue script

echo.
echo Press any key to exit...
pause >nul
