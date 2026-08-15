# MarkItDown Web

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-TW.md">繁體中文</a>
</p>

<p align="center">
  <a href="#usage">Usage</a> · <a href="#architecture">Architecture</a> · <a href="#development">Development</a> · <a href="#security-boundary">Security</a>
</p>

<p align="center">
  <img alt="version 1.0.0" src="https://img.shields.io/badge/version-1.0.0-orange">
  <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white">
  <img alt="Conda md_webui" src="https://img.shields.io/badge/conda-md__webui-44A833?logo=anaconda&logoColor=white">
  <a href="LICENSE"><img alt="license MIT" src="https://img.shields.io/badge/license-MIT-green"></a>
</p>

A lightweight local web interface powered by Microsoft MarkItDown. Upload a document to view its Markdown source and rendered preview side by side; edit, copy, and download the result. The interface defaults to en-US and can be switched to zh-TW with the language button.

## Usage

Use Python 3.10 or newer to run the local service, then open it in a browser. The project follows the Python requirement declared by MarkItDown 0.1.7. The same commands work in Windows PowerShell, macOS, and Linux.

### uv (project setup)

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if it is not already available.

On macOS and Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows PowerShell:

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

From the repository root, create or update the project environment and start the service:

```bash
uv sync --no-dev
uv run --no-dev python run.py
```

uv manages the project-local `.venv` automatically; you do not need to run `uv venv` or activate the environment manually. The `.venv` directory is local and ignored by Git.

### Python virtual environment

From the repository root, create a virtual environment and install the dependencies:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Or activate it on macOS and Linux:

```bash
source .venv/bin/activate
```

Then start the service:

```bash
pip install -r requirements.txt
python run.py
```

### Conda / Miniconda

From the repository root:

```bash
conda env create -f environment.yml
conda activate md_webui
python run.py
```

Then open `http://localhost:8765` in your browser.

`environment.yml` creates the default Conda environment as **`md_webui`**, lets Conda manage a compatible Python version, and installs the project's Python packages from `requirements.txt` inside that environment. To refresh an existing environment after dependency changes, run:

```bash
conda env update -f environment.yml --prune
```

The service listens only on the local loopback interface and is not exposed to the LAN or internet. Stop it with `Ctrl+C` in the terminal where it is running.

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

Key files: `app/main.py` (HTTP endpoints, limits, and security headers), `app/converter.py` (stream conversion), `app/preview.py` (Markdown rendering and sanitization), `app/static/` (framework-free frontend), and `run.py` (local server entry point).

## Development

Using uv:

```bash
uv sync
uv run pytest
uv run ruff check .
uv run python run.py
```

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
conda activate md_webui-dev
pytest
ruff check .
python run.py
```

`environment-dev.yml` creates the development Conda environment as **`md_webui-dev`** and installs `requirements-dev.txt`, which includes the runtime dependencies plus the test and lint tools. The requirements files are generated exports of the uv lockfile so the venv and Conda setup paths stay aligned with the uv project.

When dependencies change, update `pyproject.toml`, run `uv lock`, and regenerate both requirements files with `uv export`.

## Security boundary

This is a local desktop tool, not a multi-tenant public upload service. Although extension, filename, and size limits are enforced and conversion uses `convert_stream()`, only trusted documents should be converted. An externally exposed deployment would need process isolation, resource quotas, ZIP extraction limits, malware scanning, and timeouts.

## Upstream and license

This project does not include Microsoft MarkItDown source code; `pyproject.toml` declares the official PyPI package `markitdown==0.1.7`, `uv.lock` records the resolved dependencies, and the supplied venv and Conda setup paths use exported requirements files. This interface is MIT licensed; third-party packages retain their respective licenses. See `THIRD_PARTY_NOTICES.md`.
