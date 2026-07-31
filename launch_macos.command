#!/bin/zsh
set -eu
cd "$(dirname "$0")"

for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$candidate" >/dev/null 2>&1; then
    if "$candidate" -c 'import sys; raise SystemExit(0 if (3,10) <= sys.version_info[:2] <= (3,13) else 1)' >/dev/null 2>&1; then
      exec "$candidate" launcher.py
    fi
  fi
done

osascript -e 'display alert "MarkItDown Web" message "需要 Python 3.10–3.13。請先安裝 Python。" as critical'
exit 1
