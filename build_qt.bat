@echo off
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
cd /d C:\qt-everywhere-src-5.15.2\build
..\configure.bat -prefix C:\Qt\5.15.2 -platform win32-msvc -opensource -confirm-license -nomake examples -nomake tests -skip qtwebengine -release -mp
if errorlevel 1 goto error
nmake
if errorlevel 1 goto error
nmake install
goto end
:error
echo Build failed!
pause
:end
