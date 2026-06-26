@echo off
setlocal EnableExtensions

cd /d "%~dp0"

echo [1/3] Instalando dependencias...
python -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo [2/3] Limpiando compilaciones anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "SolarEduPV.spec" del /q "SolarEduPV.spec"

set "PYINSTALLER_ARGS=--noconfirm --clean --onedir --name SolarEduPV --collect-all streamlit --collect-all pvlib --add-data ""app.py;."""

if exist "core" set "PYINSTALLER_ARGS=%PYINSTALLER_ARGS% --add-data ""core;core"""
if exist "components" set "PYINSTALLER_ARGS=%PYINSTALLER_ARGS% --add-data ""components;components"""
if exist "data" set "PYINSTALLER_ARGS=%PYINSTALLER_ARGS% --add-data ""data;data"""
if exist "assets" set "PYINSTALLER_ARGS=%PYINSTALLER_ARGS% --add-data ""assets;assets"""
if exist ".streamlit" set "PYINSTALLER_ARGS=%PYINSTALLER_ARGS% --add-data "".streamlit;.streamlit"""

echo [3/3] Generando SolarEduPV.exe...
python -m PyInstaller %PYINSTALLER_ARGS% launcher.py
if errorlevel 1 goto :error

echo.
echo Compilacion completada.
echo Ejecutable: dist\SolarEduPV\SolarEduPV.exe
exit /b 0

:error
echo.
echo El proceso de compilacion fallo. Revise los mensajes anteriores.
exit /b 1
