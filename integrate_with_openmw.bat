@echo off
REM Morrowind AI Framework - OpenMW Integration Script
REM This script automates the integration of the Morrowind AI Framework with OpenMW

echo Morrowind AI Framework - OpenMW Integration Script
echo ===================================================

REM Set paths
set FRAMEWORK_DIR=%~dp0
set OPENMW_DIR=
set OPENMW_BUILD_DIR=

REM Ask for OpenMW source directory
echo.
echo Please enter the path to your OpenMW source directory:
set /p OPENMW_DIR=

REM Validate OpenMW directory
if not exist "%OPENMW_DIR%\CMakeLists.txt" (
    echo Error: Invalid OpenMW directory. CMakeLists.txt not found.
    goto :end
)

REM Check OpenMW version
echo.
echo Checking OpenMW version...
findstr /C:"Version: 0.49.0" "%OPENMW_DIR%\README.md" >nul
if %ERRORLEVEL% neq 0 (
    echo Warning: This integration is designed for OpenMW 0.49.0.
    echo Current version may be different. Continue at your own risk.
    echo.
    echo Do you want to continue? (y/n)
    set /p CONTINUE=
    if /i not "%CONTINUE%"=="y" goto :end
)

REM Create backup
echo.
echo Creating backup of original files...
if not exist "%OPENMW_DIR%\backup" mkdir "%OPENMW_DIR%\backup"
copy "%OPENMW_DIR%\apps\openmw\engine.cpp" "%OPENMW_DIR%\backup\engine.cpp.bak"
copy "%OPENMW_DIR%\apps\openmw\engine.hpp" "%OPENMW_DIR%\backup\engine.hpp.bak"
copy "%OPENMW_DIR%\apps\openmw\mwbase\environment.cpp" "%OPENMW_DIR%\backup\environment.cpp.bak"
copy "%OPENMW_DIR%\apps\openmw\mwbase\environment.hpp" "%OPENMW_DIR%\backup\environment.hpp.bak"
copy "%OPENMW_DIR%\components\CMakeLists.txt" "%OPENMW_DIR%\backup\CMakeLists.txt.bak"

REM Create integration branch
echo.
echo Creating integration branch...
cd "%OPENMW_DIR%"
git checkout -b morrowind-ai-integration

REM Copy AI components
echo.
echo Copying AI components to OpenMW source tree...
if not exist "%OPENMW_DIR%\components\ai_client" mkdir "%OPENMW_DIR%\components\ai_client"
xcopy /E /Y "%FRAMEWORK_DIR%\openmw-client\components\ai_client\*" "%OPENMW_DIR%\components\ai_client\"

if not exist "%OPENMW_DIR%\components\openmw-mp\mwbase" mkdir "%OPENMW_DIR%\components\openmw-mp\mwbase"
xcopy /E /Y "%FRAMEWORK_DIR%\openmw-client\components\openmw-mp\*" "%OPENMW_DIR%\components\openmw-mp\"

REM Copy Lua scripts
echo.
echo Copying Lua scripts to OpenMW resources...
if not exist "%OPENMW_DIR%\resources\lua" mkdir "%OPENMW_DIR%\resources\lua"
xcopy /E /Y "%FRAMEWORK_DIR%\openmw-client\resources\lua\*" "%OPENMW_DIR%\resources\lua\"

REM Apply patch
echo.
echo Applying patch to OpenMW engine...
cd "%OPENMW_DIR%"
git apply "%FRAMEWORK_DIR%\openmw-source\apps\openmw\engine.cpp.patch"
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to apply patch. Please check if the patch is compatible with your OpenMW version.
    goto :end
)

REM Update CMakeLists.txt
echo.
echo Updating CMake configuration...
echo add_component_dir(ai_client client) >> "%OPENMW_DIR%\components\CMakeLists.txt"

REM Create build directory
echo.
echo Setting up build directory...
if not exist "%OPENMW_DIR%\build" mkdir "%OPENMW_DIR%\build"
set OPENMW_BUILD_DIR=%OPENMW_DIR%\build

REM Configure and build
echo.
echo Do you want to configure and build OpenMW now? (y/n)
set /p BUILD=
if /i "%BUILD%"=="y" (
    echo.
    echo Configuring build...
    cd "%OPENMW_BUILD_DIR%"
    cmake ..
    
    echo.
    echo Building OpenMW...
    cmake --build . --config Release
)

REM Create configuration file
echo.
echo Creating AI configuration for OpenMW...
echo # AI Framework Configuration > "%OPENMW_BUILD_DIR%\ai_config.cfg"
echo enable lua = true >> "%OPENMW_BUILD_DIR%\ai_config.cfg"
echo lua ai_npc_dialogue.lua >> "%OPENMW_BUILD_DIR%\ai_config.cfg"
echo ai server host = localhost >> "%OPENMW_BUILD_DIR%\ai_config.cfg"
echo ai server port = 8082 >> "%OPENMW_BUILD_DIR%\ai_config.cfg"
echo.
echo Add the contents of ai_config.cfg to your openmw.cfg file.

echo.
echo Integration completed successfully!
echo.
echo Next steps:
echo 1. Start the AI server: %FRAMEWORK_DIR%\ai-server\start_server.bat
echo 2. Launch OpenMW with the AI integration
echo 3. Test with an NPC that has the AIDialogue script

:end
echo.
echo Press any key to exit...
pause >nul
