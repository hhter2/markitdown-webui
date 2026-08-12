# MarkItDown Web

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-TW.md">繁體中文</a>
</p>

<p align="center">
  <a href="#usage">Usage</a> · <a href="#architecture">Architecture</a> · <a href="#development">Development</a> · <a href="#security-boundary">Security</a>
</p>

<p align="center">
  <img alt="version 1.0.0" src="https://img.shields.io/badge/version-1.0.0-orange">
  <img alt="Python 3.10-3.13" src="https://img.shields.io/badge/python-3.10--3.13-blue?logo=python&logoColor=white">
  <img alt="Conda md_webui" src="https://img.shields.io/badge/conda-md__webui-44A833?logo=anaconda&logoColor=white">
  <a href="LICENSE"><img alt="license MIT" src="https://img.shields.io/badge/license-MIT-green"></a>
</p>

A lightweight local web interface powered by Microsoft MarkItDown. Upload a document to view its Markdown source and rendered preview side by side; edit, copy, and download the result. The interface defaults to en-US and can be switched to zh-TW with the language button.

## Usage

There are two supported ways to run the project:

- **Desktop launcher:** requires **Python 3.10–3.13** and an internet connection on first launch. The launcher creates `.runtime/venv` and installs the pinned runtime dependencies automatically.
- **Conda / Miniconda:** create the supplied Conda environment and run the service directly from that environment.

### Windows

Double-click `Start MarkItDown Web.vbs`. The browser opens automatically after setup completes.

### macOS

Double-click `MarkItDown Web.app`. If macOS blocks the unsigned app, Control-click it and choose “Open” the first time. You can also run `launch_macos.command`.

### Linux

Run `launch_linux.sh`. On a desktop environment, make it executable and double-click it.

### Conda / Miniconda

From the repository root:

```bash
conda env create -f environment.yml
conda activate md_webui
python run.py
```

Then open `http://127.0.0.1:8765` if the browser is not opened manually.

`environment.yml` creates the default Conda environment as **`md_webui`**, lets Conda manage a compatible Python version, and installs the project's Python packages from `requirements.txt` inside that environment. To refresh an existing environment after dependency changes, run:

```bash
conda env update -f environment.yml --prune
```

If you want to run **inside the active Conda environment**, use `python run.py`. The platform launchers intentionally use the private `.runtime/venv` runtime instead of the currently activated Conda environment.

The service listens only on `127.0.0.1:8765` and is not exposed to the LAN or internet. If an instance is already running, the desktop launcher opens the existing page.

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

Using `venv`:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
pytest
python run.py
```

Using Conda:

```bash
conda env create -f environment-dev.yml
conda activate markitdown-webui-dev
pytest
ruff check .
python run.py
```

`environment-dev.yml` installs `requirements-dev.txt`, which includes the runtime dependencies plus the test and lint tools.

## Security boundary

This is a local desktop tool, not a multi-tenant public upload service. Although extension, filename, and size limits are enforced and conversion uses `convert_stream()`, only trusted documents should be converted. An externally exposed deployment would need process isolation, resource quotas, ZIP extraction limits, malware scanning, and timeouts.

## Upstream and license

This project does not include Microsoft MarkItDown source code; it installs the official PyPI package `markitdown==0.1.7` on first launch or when the selected environment is created. This interface is MIT licensed; third-party packages retain their respective licenses. See `THIRD_PARTY_NOTICES.md`.
