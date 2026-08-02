@echo off
setlocal EnableExtensions

if exist .env (
  for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
    if not "%%A"=="" if not "%%A:~0,1%"=="#" set "%%A=%%B"
  )
)

if "%OMNIROUTE_BASE_URL%"=="" set "OMNIROUTE_BASE_URL=http://localhost:20128/v1"
if "%OMNIROUTE_API_KEY%"=="" set "OMNIROUTE_API_KEY="
if "%OMNIROUTE_MODEL%"=="" set "OMNIROUTE_MODEL=auto/best-fast"
if "%OMNIROUTE_API_PATH%"=="" set "OMNIROUTE_API_PATH=/chat/completions"

set "ANTHROPIC_BASE_URL=%OMNIROUTE_BASE_URL%"
set "ANTHROPIC_API_KEY=%OMNIROUTE_API_KEY%"
set "ANTHROPIC_MODEL=%OMNIROUTE_MODEL%"
set "OPENAI_BASE_URL=%OMNIROUTE_BASE_URL%"
set "OPENAI_API_KEY=%OMNIROUTE_API_KEY%"
set "OPENAI_MODEL=%OMNIROUTE_MODEL%"

set "NPM_BIN=%APPDATA%\npm"
if exist "%NPM_BIN%" set "PATH=%NPM_BIN%;%PATH%"

where claude >nul 2>nul
if errorlevel 1 (
  echo Claude Code CLI was not found on PATH.
  echo Install Claude Code or add its executable to PATH, then rerun this script.
  exit /b 1
)

claude %*
exit /b %errorlevel%
