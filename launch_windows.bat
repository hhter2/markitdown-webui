@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 (
  for %%V in (3.13 3.12 3.11 3.10) do (
    py -%%V -c "import sys; raise SystemExit(0 if (3,10) <= sys.version_info[:2] <= (3,13) else 1)" >nul 2>nul
    if !errorlevel! EQU 0 (
      py -%%V launcher.py
      exit /b !errorlevel!
    )
  )
)

where python >nul 2>nul
if not errorlevel 1 (
  python launcher.py
  exit /b !errorlevel!
)

mshta "javascript:alert('需要 Python 3.10–3.13。請先從 python.org 安裝 Python。');close();"
exit /b 1
