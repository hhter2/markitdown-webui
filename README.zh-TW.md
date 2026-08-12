# MarkItDown Web

<p><a href="README.md">English</a> · <a href="README.zh-TW.md">繁體中文</a></p>

一個以 Microsoft MarkItDown 為核心的輕量本機 Web 介面。使用者可以上傳文件，並排查看 Markdown 原始碼與渲染效果；原始碼可直接編輯、複製及下載。介面預設為 en-US，也可以使用語言按鈕切換至 zh-TW。

## 使用方式

本專案支援兩種執行方式：

- **桌面啟動器：**需要 **Python 3.10–3.13** 與首次啟動時的網路連線。啟動器會自行建立 `.runtime/venv` 並安裝固定版本的執行依賴。
- **Conda / Miniconda：**使用專案提供的 Conda 環境檔建立環境，並直接從該環境執行服務。

### Windows

雙擊 `Start MarkItDown Web.vbs`。背景安裝完成後，瀏覽器會自動開啟。

### macOS

雙擊 `MarkItDown Web.app`。若 macOS 阻擋未簽署 App，第一次可按住 Control 點擊並選擇「打開」。也可執行 `launch_macos.command`。

### Linux

執行 `launch_linux.sh`。桌面環境可將此檔案設為可執行後雙擊。

### Conda / Miniconda

在 repository 根目錄執行：

```bash
conda env create -f environment.yml
conda activate markitdown-webui
python run.py
```

若瀏覽器沒有自動開啟，請前往 `http://127.0.0.1:8765`。

`environment.yml` 會讓 Conda 管理相容的 Python 版本，並在該環境內透過 `requirements.txt` 安裝專案所需的 Python 套件。依賴更新後，可用以下指令更新既有環境：

```bash
conda env update -f environment.yml --prune
```

若你希望程式**確實執行在目前啟用的 Conda 環境中**，請使用 `python run.py`。各平台桌面啟動器是刻意設計成使用獨立的 `.runtime/venv`，不會沿用目前啟用的 Conda 環境。

服務只監聽 `127.0.0.1:8765`，不對區域網路或網際網路開放。若已有實例執行，桌面啟動器只會開啟既有頁面。

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

主要檔案：`app/main.py`（HTTP 端點、大小限制與安全標頭）、`app/converter.py`（MarkItDown 串流轉換封裝）、`app/preview.py`（Markdown 渲染與 HTML 清理）、`app/static/`（無框架前端）與 `launcher.py`（跨平台私有執行環境管理）。

## 開發

使用 `venv`：

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
pytest
python run.py
```

使用 Conda：

```bash
conda env create -f environment-dev.yml
conda activate markitdown-webui-dev
pytest
ruff check .
python run.py
```

`environment-dev.yml` 會安裝 `requirements-dev.txt`，其中包含執行階段依賴、測試與 lint 工具。

開發指令只提供給維護者；一般使用者不需執行。

## 安全邊界

這是本機桌面用途工具，不是多租戶公開上傳服務。雖然已限制副檔名、檔名與大小，且只使用 `convert_stream()`，仍應只轉換可信文件。若改成對外服務，必須增加程序隔離、資源配額、ZIP 解壓限制、惡意檔案掃描與逾時終止。

## 上游與授權

本專案不包含 Microsoft MarkItDown 的原始碼；桌面啟動器首次啟動時，或建立指定的 Python/Conda 環境時，會安裝官方 PyPI 套件 `markitdown==0.1.7`。本介面採 MIT License；第三方套件各自依原授權使用。詳見 `THIRD_PARTY_NOTICES.md`。
