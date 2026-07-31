from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.request
import webbrowser

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / ".runtime"
VENV = RUNTIME / "venv"
LOG = RUNTIME / "launcher.log"
STAMP = RUNTIME / "requirements.sha256"
PORT = int(os.environ.get("MARKITDOWN_WEB_PORT", "8765"))
URL = f"http://127.0.0.1:{PORT}"


def main() -> int:
    RUNTIME.mkdir(exist_ok=True)
    if not (3, 10) <= sys.version_info[:2] <= (3, 13):
        return fail("需要 Python 3.10–3.13。請安裝後再重新啟動。")

    if health_ready():
        webbrowser.open(URL)
        return 0

    try:
        ensure_runtime()
        process = subprocess.Popen(
            [str(venv_python()), str(ROOT / "run.py")],
            cwd=ROOT,
            stdout=open(LOG, "a", encoding="utf-8"),
            stderr=subprocess.STDOUT,
            creationflags=_creation_flags(),
        )
        if wait_until_ready(process):
            webbrowser.open(URL)
            return process.wait()
        process.terminate()
        return fail(f"服務未能啟動。詳細資訊：{LOG}")
    except Exception as exc:
        return fail(f"啟動失敗：{exc}\n\n詳細資訊：{LOG}")


def ensure_runtime() -> None:
    requirements = ROOT / "requirements.txt"
    digest = hashlib.sha256(requirements.read_bytes()).hexdigest()
    current = STAMP.read_text(encoding="utf-8").strip() if STAMP.exists() else ""

    if not venv_python().exists():
        log("建立私有執行環境…")
        subprocess.run([sys.executable, "-m", "venv", str(VENV)], check=True)
        current = ""

    if current != digest:
        log("安裝或更新所需套件…")
        subprocess.run(
            [
                str(venv_python()),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--upgrade",
                "pip",
            ],
            cwd=ROOT,
            check=True,
            stdout=open(LOG, "a", encoding="utf-8"),
            stderr=subprocess.STDOUT,
        )
        subprocess.run(
            [
                str(venv_python()),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "-r",
                str(requirements),
            ],
            cwd=ROOT,
            check=True,
            stdout=open(LOG, "a", encoding="utf-8"),
            stderr=subprocess.STDOUT,
        )
        STAMP.write_text(digest, encoding="utf-8")


def venv_python() -> Path:
    if os.name == "nt":
        return VENV / "Scripts" / "python.exe"
    return VENV / "bin" / "python"


def health_ready() -> bool:
    try:
        with urllib.request.urlopen(f"{URL}/api/health", timeout=0.4) as response:
            return response.status == 200
    except Exception:
        return False


def wait_until_ready(process: subprocess.Popen[bytes], timeout: float = 90.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            return False
        if health_ready():
            return True
        time.sleep(0.25)
    return False


def log(message: str) -> None:
    RUNTIME.mkdir(exist_ok=True)
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")


def fail(message: str) -> int:
    log(message)
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("MarkItDown Web", message)
        root.destroy()
    except Exception:
        print(message, file=sys.stderr)
    return 1


def _creation_flags() -> int:
    if os.name != "nt":
        return 0
    return getattr(subprocess, "CREATE_NO_WINDOW", 0)


if __name__ == "__main__":
    raise SystemExit(main())
