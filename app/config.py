from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _bounded_int(raw: str | None, *, default: int, low: int, high: int) -> int:
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return min(max(value, low), high)


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str = "MarkItDown Web"
    host: str = "127.0.0.1"
    port: int = 8765
    max_upload_bytes: int = 64 * 1024 * 1024
    max_markdown_chars: int = 4_000_000

    @classmethod
    def from_env(cls) -> "Settings":
        max_mb = _bounded_int(os.getenv("MARKITDOWN_WEB_MAX_MB"), default=64, low=1, high=512)
        port = _bounded_int(os.getenv("MARKITDOWN_WEB_PORT"), default=8765, low=1024, high=65535)
        return cls(port=port, max_upload_bytes=max_mb * 1024 * 1024)


BASE_DIR = Path(__file__).resolve().parent
SETTINGS = Settings.from_env()
