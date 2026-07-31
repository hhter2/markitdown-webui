from fastapi.testclient import TestClient

import app.main as main_module

client = TestClient(main_module.app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_convert_upload(monkeypatch) -> None:
    monkeypatch.setattr(main_module, "convert_bytes", lambda data, extension: "# Converted\n")
    response = client.post(
        "/api/convert",
        files={"file": ("notes.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["filename"] == "notes.txt"
    assert payload["output_filename"] == "notes.md"
    assert payload["markdown"] == "# Converted\n"


def test_rejects_unknown_extension() -> None:
    response = client.post(
        "/api/convert",
        files={"file": ("malware.exe", b"not really", "application/octet-stream")},
    )
    assert response.status_code == 400
