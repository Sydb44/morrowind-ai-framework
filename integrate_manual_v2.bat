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
(
    echo # AI Framework Configuration
    echo enable lua = true
    echo lua ai_npc_dialogue.lua
    echo ai server host = localhost
    echo ai server port = 8082
) > "%OPENMW_DIR%\build\ai_config.cfg"

echo.
echo Modifying OpenMW engine files...

REM Modify engine.hpp
set ENGINE_HPP=%OPENMW_DIR%\apps\openmw\engine.hpp
findstr /i /c:"class AIManager;" "%ENGINE_HPP%" > nul
if errorlevel 1 (
    echo class AIManager; >> "%ENGINE_HPP%"
)
findstr /i /c:"MWBase::AIManager* mAIManager;" "%ENGINE_HPP%" > nul
if errorlevel 1 (
    echo MWBase::AIManager* mAIManager; >> "%ENGINE_HPP%"
)

REM Modify engine.cpp
set ENGINE_CPP=%OPENMW_DIR%\apps\openmw\engine.cpp
findstr /i /c:"#include <components/openmw-mp/mwbase/aimanagerimpl.hpp>" "%ENGINE_CPP%" > nul
if errorlevel 1 (
    echo #include ^<components/openmw-mp/mwbase/aimanagerimpl.hpp^> >> "%ENGINE_CPP%"
)

REM Add AIManager initialization after mState initialization
findstr /i /c:"mState = new MWState::StateManager" "%ENGINE_CPP%" > nul
if not errorlevel 1 (
    echo.>> "%ENGINE_CPP%"
    echo // AI Manager>> "%ENGINE_CPP%"
    echo std::string aiServerHost = mCfgMgr.getStringOption("ai server host", "localhost");>> "%ENGINE_CPP%"
    echo int aiServerPort = mCfgMgr.getIntOption("ai server port", 8080);>> "%ENGINE_CPP%"
    echo.>> "%ENGINE_CPP%"
    echo mAIManager = new MWBase::AIManagerImpl();>> "%ENGINE_CPP%"
    echo mAIManager-^>init(aiServerHost, aiServerPort);>> "%ENGINE_CPP%"
    echo mEnvironment.setAIManager(mAIManager);>> "%ENGINE_CPP%"
)

REM Modify environment files
set ENV_HPP=%OPENMW_DIR%\apps\openmw\mwbase\environment.hpp
findstr /i /c:"AIManager* mAIManager;" "%ENV_HPP%" > nul
if errorlevel 1 (
    echo AIManager* mAIManager; >> "%ENV_HPP%"
)

set ENV_CPP=%OPENMW_DIR%\apps\openmw\mwbase\environment.cpp
findstr /i /c:"void Environment::setAIManager" "%ENV_CPP%" > nul
if errorlevel 1 (
    echo void Environment::setAIManager(AIManager* manager) { mAIManager = manager; } >> "%ENV_CPP%"
)

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
