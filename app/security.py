from __future__ import annotations

from pathlib import Path

ALLOWED_EXTENSIONS = frozenset(
    {
        ".pdf",
        ".docx",
        ".pptx",
        ".xlsx",
        ".xls",
        ".html",
        ".htm",
        ".csv",
        ".json",
        ".xml",
        ".txt",
        ".md",
        ".epub",
        ".msg",
        ".zip",
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp",
        ".wav",
        ".mp3",
        ".m4a",
    }
)


def safe_filename(filename: str | None) -> str:
    if not filename:
        raise ValueError("檔案缺少名稱。")
    normalized = filename.replace("\\", "/")
    basename = Path(normalized).name.strip()
    if not basename or basename in {".", ".."}:
        raise ValueError("檔案名稱無效。")
    if len(basename) > 240:
        raise ValueError("檔案名稱過長。")
    return basename


def validate_extension(filename: str) -> str:
    extension = Path(filename).suffix.lower()
    if not extension or extension not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        raise ValueError(f"不支援此檔案格式。可用格式：{allowed}")
    return extension


def output_filename(source_filename: str) -> str:
    stem = Path(source_filename).stem.strip() or "converted"
    cleaned = "".join(ch for ch in stem if ch not in '<>:"/\\|?*\0').strip(" .")
    return f"{cleaned or 'converted'}.md"
