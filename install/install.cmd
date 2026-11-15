@echo off
rem Windows entry point for install.ps1. Works by double-click or from cmd/PowerShell.
rem -ExecutionPolicy Bypass applies only to this run; it does not change system settings.
setlocal
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" %*
set "KOKORO_EXIT=%ERRORLEVEL%"
if "%~1"=="" if not defined KOKORO_NO_PAUSE pause
exit /b %KOKORO_EXIT%
