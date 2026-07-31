# MarkItDown Web

<p><a href="README.md">English</a> · <a href="README.zh-TW.md">繁體中文</a></p>

A lightweight local web interface powered by Microsoft MarkItDown. Upload a document to view its Markdown source and rendered preview side by side; edit, copy, and download the result. The interface defaults to en-US and can be switched to zh-TW with the language button.

## Usage

The only prerequisites are **Python 3.10–3.13** and an internet connection on first launch. The launcher creates `.runtime/venv` and installs a pinned MarkItDown version automatically; users do not need to run `pip`, create a virtual environment, or open a command prompt.

### Windows

Double-click `Start MarkItDown Web.vbs`. The browser opens automatically after setup completes.

### macOS

Double-click `MarkItDown Web.app`. If macOS blocks the unsigned app, Control-click it and choose “Open” the first time. You can also run `launch_macos.command`.

### Linux

Run `launch_linux.sh`. On a desktop environment, make it executable and double-click it.

The service listens only on `127.0.0.1:8765` and is not exposed to the LAN or internet. If an instance is already running, the launcher opens the existing page.

## Features

- Drag and drop or choose one document.
- Convert via an in-memory stream without writing the uploaded original to disk.
- Show Markdown source and rendered preview side by side.
- Update the preview live while editing.
- Copy or download the edited `.md`.
- 64 MB default limit, configurable from 1–512 MB with `MARKITDOWN_WEB_MAX_MB`.
- Sanitize preview HTML and disable raw HTML in Markdown.

Supported formats depend on the installed MarkItDown components. This project includes the extras commonly needed for local documents: PDF, DOCX, PPTX, XLSX, XLS, Outlook MSG, plus core support for HTML, CSV, JSON, XML, text, EPUB, ZIP, images, and some audio metadata. Cloud analysis, LLM image descriptions, and audio transcription are not enabled to reduce installation size and external-service dependencies.

## Architecture

```text
Browser
  ├─ POST /api/convert  ──> FastAPI ──> MarkItDown.convert_stream()
  ├─ POST /api/render   ──> markdown-it-py ──> Bleach sanitization
  └─ Blob download      ──> Markdown edited by the user
```

Key files: `app/main.py` (HTTP endpoints, limits, and security headers), `app/converter.py` (stream conversion), `app/preview.py` (Markdown rendering and sanitization), `app/static/` (framework-free frontend), and `launcher.py` (cross-platform private runtime management).

## Development

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
pytest
python run.py
```

## Security boundary

This is a local desktop tool, not a multi-tenant public upload service. Although extension, filename, and size limits are enforced and conversion uses `convert_stream()`, only trusted documents should be converted. An externally exposed deployment would need process isolation, resource quotas, ZIP extraction limits, malware scanning, and timeouts.

## Upstream and license

This project does not include Microsoft MarkItDown source code; it installs the official PyPI package `markitdown==0.1.7` on first launch. This interface is MIT licensed; third-party packages retain their respective licenses. See `THIRD_PARTY_NOTICES.md`.
