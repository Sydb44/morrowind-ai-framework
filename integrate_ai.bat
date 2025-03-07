@echo off
setlocal enabledelayedexpansion

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
echo Applying AI integration patch...
cd "%OPENMW_DIR%"
git apply "%OPENMW_DIR%\ai_integration.patch"

echo.
echo Integration completed!
echo.
echo Next steps:
echo 1. Configure and build OpenMW:
echo    cd %OPENMW_DIR%\build
echo    cmake ..
echo    cmake --build . --config Release
echo.
echo 2. Start the AI server:
echo    %BASE_DIR%\ai-server\start_server.bat
echo.
echo 3. Launch OpenMW with the AI integration
echo.
echo 4. Test with an NPC that has the AIDialogue script

echo.
echo Press any key to exit...
pause >nul
