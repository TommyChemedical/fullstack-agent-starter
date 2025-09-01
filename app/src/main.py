from fastapi import FastAPI
import os

app = FastAPI(title="EdTech Backend", version="0.1.0")

# Telemetry optional aktivieren (falls vorhanden)
try:
    from app.src.middleware.telemetry import TelemetryMiddleware  # type: ignore
    if os.getenv("TELEMETRY_ENABLED", "1") not in ("0", "false", "False"):
        app.add_middleware(TelemetryMiddleware)
except Exception:
    pass

# Health
@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "version": "0.1.0", "agent": "ready"}

# Courses-Router (falls vorhanden)
try:
    from app.src.api.routers.courses import router as courses_router  # type: ignore
    app.include_router(courses_router)
except Exception:
    pass
