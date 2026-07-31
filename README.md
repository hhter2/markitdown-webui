# MarkItDown Web

## English

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

## 繁體中文

一個以 Microsoft MarkItDown 為核心的輕量本機 Web 介面。使用者可以上傳文件，並排查看 Markdown 原始碼與渲染效果；原始碼可直接編輯、複製及下載。

## 使用方式

前置需求只有 **Python 3.10–3.13** 與首次啟動時的網路連線。啟動器會自行建立 `.runtime/venv`、安裝固定版本的 MarkItDown，使用者不需要執行 `pip`、建立 venv 或開啟命令提示字元。

### Windows

雙擊 `Start MarkItDown Web.vbs`。背景安裝完成後，瀏覽器會自動開啟。

### macOS

雙擊 `MarkItDown Web.app`。若 macOS 阻擋未簽署 App，第一次可按住 Control 點擊並選擇「打開」。也可執行 `launch_macos.command`。

### Linux

執行 `launch_linux.sh`。桌面環境可將此檔案設為可執行後雙擊。

服務只監聽 `127.0.0.1:8765`，不對區域網路或網際網路開放。若已有實例執行，啟動器只會開啟既有頁面。

## 功能

- 拖放或選取單一文件。
- 使用記憶體串流轉換，不把上傳原始檔寫入磁碟。
- Markdown 程式碼與渲染預覽並排顯示。
- 編輯時即時更新預覽。
- 複製或下載編輯後的 `.md`。
- 64 MB 預設上限，可透過 `MARKITDOWN_WEB_MAX_MB` 調整至 1–512 MB。
- 預覽 HTML 經清理，且停用 Markdown 內嵌 HTML。

支援格式由安裝的 MarkItDown 元件決定。本專案採用常見本機文件格式所需的 extras：PDF、DOCX、PPTX、XLSX、XLS、Outlook MSG，以及核心支援的 HTML、CSV、JSON、XML、文字、EPUB、ZIP、圖片與部分音訊中繼資料。雲端分析、LLM 圖像描述與音訊轉錄未啟用，以降低安裝體積與外部服務依賴。

## 架構

```text
瀏覽器
  ├─ POST /api/convert  ──> FastAPI ──> MarkItDown.convert_stream()
  ├─ POST /api/render   ──> markdown-it-py ──> Bleach 清理
  └─ Blob 下載          ──> 使用者編輯後的 Markdown
```

主要檔案：

- `app/main.py`：HTTP 端點、大小限制與安全標頭。
- `app/converter.py`：MarkItDown 串流轉換封裝。
- `app/preview.py`：Markdown 渲染與 HTML 清理。
- `app/static/`：無框架前端。
- `launcher.py`：跨平台私有執行環境管理。

## 開發

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
pytest
python run.py
```

開發指令只提供給維護者；一般使用者不需執行。

## 安全邊界

這是本機桌面用途工具，不是多租戶公開上傳服務。雖然已限制副檔名、檔名與大小，且只使用 `convert_stream()`，仍應只轉換可信文件。若改成對外服務，必須增加程序隔離、資源配額、ZIP 解壓限制、惡意檔案掃描與逾時終止。

## 上游與授權

本專案不包含 Microsoft MarkItDown 的原始碼，而是在首次啟動時安裝官方 PyPI 套件 `markitdown==0.1.7`。本介面採 MIT License；第三方套件各自依原授權使用。詳見 `THIRD_PARTY_NOTICES.md`。
