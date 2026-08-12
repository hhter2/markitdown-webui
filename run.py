from __future__ import annotations

import uvicorn

from app.config import SETTINGS


if __name__ == "__main__":
    print(f"Server started at http://localhost:{SETTINGS.port}", flush=True)
    uvicorn.run(
        "app.main:app",
        host=SETTINGS.host,
        port=SETTINGS.port,
        reload=False,
        access_log=False,
        log_level="warning",
    )
