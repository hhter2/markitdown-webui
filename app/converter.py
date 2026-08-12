from __future__ import annotations

from io import BytesIO
from typing import Any


def convert_bytes(data: bytes, extension: str) -> str:
    """Convert an in-memory upload using MarkItDown's stream API."""
    try:
        from markitdown import MarkItDown, StreamInfo
    except ImportError as exc:  # pragma: no cover - dependency installation issue
        raise RuntimeError("MarkItDown 尚未安裝，請執行 pip install -r requirements.txt。") from exc

    converter = MarkItDown(enable_plugins=False)
    stream_info = StreamInfo(extension=extension)
    result: Any = converter.convert_stream(BytesIO(data), stream_info=stream_info)

    markdown = getattr(result, "markdown", None)
    if markdown is None:
        markdown = getattr(result, "text_content", None)
    if not isinstance(markdown, str):
        raise RuntimeError("轉換器未回傳 Markdown 文字。")
    return markdown
