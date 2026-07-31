from __future__ import annotations

import sys
import types

from app.converter import convert_bytes


def test_convert_bytes_uses_stream_info(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeStreamInfo:
        def __init__(self, *, extension: str):
            self.extension = extension

    class FakeMarkItDown:
        def __init__(self, *, enable_plugins: bool):
            captured["enable_plugins"] = enable_plugins

        def convert_stream(self, stream, *, stream_info):
            captured["bytes"] = stream.read()
            captured["extension"] = stream_info.extension
            return types.SimpleNamespace(markdown="# Result")

    fake_module = types.SimpleNamespace(MarkItDown=FakeMarkItDown, StreamInfo=FakeStreamInfo)
    monkeypatch.setitem(sys.modules, "markitdown", fake_module)

    assert convert_bytes(b"hello", ".txt") == "# Result"
    assert captured == {
        "enable_plugins": False,
        "bytes": b"hello",
        "extension": ".txt",
    }


def test_convert_bytes_supports_legacy_text_content(monkeypatch) -> None:
    class FakeStreamInfo:
        def __init__(self, *, extension: str):
            self.extension = extension

    class FakeMarkItDown:
        def __init__(self, *, enable_plugins: bool):
            pass

        def convert_stream(self, stream, *, stream_info):
            return types.SimpleNamespace(text_content="legacy")

    fake_module = types.SimpleNamespace(MarkItDown=FakeMarkItDown, StreamInfo=FakeStreamInfo)
    monkeypatch.setitem(sys.modules, "markitdown", fake_module)

    assert convert_bytes(b"hello", ".txt") == "legacy"
