@echo off
setlocal enabledelayedexpansion

echo Morrowind AI Framework - OpenMW Build Script
echo ==========================================

REM Set paths
set OPENMW_DIR=f:/Projects/morrowind_ai_framework/openmw-source
set BUILD_DIR=%OPENMW_DIR%/build
set QT_DIR=C:/ffs/5.15.2/msvc2019_64
set VCPKG_DIR=C:/vcpkg

REM Verify required paths exist
if not exist "%OPENMW_DIR%" (
    echo Error: OpenMW source directory not found at %OPENMW_DIR%
    goto error
)

if not exist "%QT_DIR%" (
    echo Error: Qt directory not found at %QT_DIR%
    goto error
)

if not exist "%VCPKG_DIR%" (
    echo Error: vcpkg directory not found at %VCPKG_DIR%
    goto error
)

echo.
echo Step 1: Installing required vcpkg packages...
cd /d %VCPKG_DIR%
vcpkg install luajit:x64-windows
vcpkg install sqlite3:x64-windows
vcpkg install bullet3:x64-windows
vcpkg install sdl2:x64-windows
vcpkg install mygui:x64-windows
vcpkg install freetype:x64-windows
vcpkg install libjpeg-turbo:x64-windows
vcpkg install libpng:x64-windows
vcpkg integrate install

echo.
echo Step 2: Cleaning build directory...
if exist "%BUILD_DIR%" (
    echo Removing existing build files...
    rd /s /q "%BUILD_DIR%"
    if errorlevel 1 (
        echo Error: Failed to clean build directory
        goto error
    )
)
mkdir "%BUILD_DIR%"
if errorlevel 1 (
    echo Error: Failed to create build directory
    goto error
)

echo.
echo Step 3: Configuring CMake...
cd /d "%BUILD_DIR%"

cmake "%OPENMW_DIR%" -G "Visual Studio 17 2022" ^
    -A x64 ^
    -DCMAKE_PREFIX_PATH="%QT_DIR%" ^
    -DCMAKE_TOOLCHAIN_FILE="%VCPKG_DIR%/scripts/buildsystems/vcpkg.cmake" ^
    -DBUILD_OPENCS=OFF ^
    -DOPENMW_USE_SYSTEM_YAML_CPP=OFF ^
    -DOPENMW_USE_SYSTEM_RECASTNAVIGATION=OFF ^
    -DOPENMW_USE_SYSTEM_OSG=OFF ^
    -DCMAKE_POLICY_DEFAULT_CMP0091=NEW ^
    -DOPENMW_USE_FFMPEG=OFF ^
    -DCMAKE_POLICY_DEFAULT_CMP0074=NEW ^
    -DCMAKE_POLICY_DEFAULT_CMP0069=NEW ^
    -DCMAKE_POLICY_DEFAULT_CMP0077=NEW ^
    -DLuaJit_LIBRARY="%VCPKG_DIR%/installed/x64-windows/lib/lua51.lib" ^
    -DSQLite3_INCLUDE_DIR="%VCPKG_DIR%/installed/x64-windows/include" ^
    -DSQLite3_LIBRARY="%VCPKG_DIR%/installed/x64-windows/lib/sqlite3.lib" ^
    -DCMAKE_POLICY_DEFAULT_CMP0057=NEW ^
    -DCMAKE_POLICY_VERSION_MINIMUM=3.16 ^
    -DCMAKE_POLICY_VERSION=3.16 ^
    -DOPENMW_OSG_STATIC_PLUGINS=OFF ^
    -DOPENMW_USE_SYSTEM_COLLADA=OFF ^
    -DBUILD_OSG=ON ^
    -DBUILD_OSG_PLUGINS=ON ^
    -DBUILD_OSG_EXAMPLES=OFF ^
    -DBUILD_OSG_APPLICATIONS=OFF ^
    -DBUILD_OSG_DEPRECATED_SERIALIZERS=OFF ^
    -DOSG_USE_LOCAL_LUA=ON ^
    -DOSG_NOTIFY_DISABLED=ON ^
    -DOSG_MSVC_VERSIONED_DLL=OFF ^
    -DOSG_DETERMINE_WIN_VERSION=OFF

if errorlevel 1 (
    echo Error: CMake configuration failed
    goto error
)

echo.
echo Step 4: Building OpenMW...
cmake --build . --config Release
if errorlevel 1 (
    echo Error: Build failed
    goto error
)

echo.
echo Build completed successfully!
echo.
echo Next steps:
echo 1. Start the AI server: %~dp0ai-server\start_server.bat
echo 2. Launch OpenMW with the AI integration
echo 3. Test with an NPC that has the AIDialogue script
goto end

:error
echo.
echo Build process failed! Please check the error messages above.
exit /b 1

:end
echo.
echo Press any key to exit...
pause >nul
