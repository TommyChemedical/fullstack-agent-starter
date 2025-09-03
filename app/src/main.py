from __future__ import annotations

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

# -----------------------------------------------------------------------------
# App-Basis
# -----------------------------------------------------------------------------
app = FastAPI(title="EdTech Backend", version="0.1.0")

# -----------------------------------------------------------------------------
# CORS (für das React-Frontend auf Vite: http://127.0.0.1:5173)
# -----------------------------------------------------------------------------
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# optionale Telemetry-Middleware (falls vorhanden)
# -----------------------------------------------------------------------------
try:
    from app.src.middleware.telemetry import TelemetryMiddleware  # type: ignore

    if os.getenv("TELEMETRY_ENABLED", "1") not in ("0", "false", "False"):
        app.add_middleware(TelemetryMiddleware)
except Exception:
    # Middleware ist optional – wenn nicht vorhanden, einfach weiter
    pass

# -----------------------------------------------------------------------------
# einfache Health-Route
# -----------------------------------------------------------------------------
@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "version": "0.1.0", "agent": "ready"}

# -----------------------------------------------------------------------------
# API-Router einbinden (Reihenfolge: zuerst die API, dann ggf. Static-Mount)
# -----------------------------------------------------------------------------
# optional: alter Demo-Router "courses", falls die Datei noch existiert
try:
    from app.src.api.routers.courses import router as courses_router  # type: ignore

    app.include_router(courses_router)
except Exception:
    pass

# Telemetry-API (GET /api/telemetry/summary)
from app.src.api.routers.telemetry import router as telemetry_router  # type: ignore

app.include_router(telemetry_router)

# Agent-API (execute/git/pr)
from app.src.api.routers.agent import router as agent_router  # type: ignore

app.include_router(agent_router)

# -----------------------------------------------------------------------------
# Frontend ausliefern (falls gebaut) ODER Root -> /docs umleiten
# -----------------------------------------------------------------------------
# Projekt-Root = .../fullstack-agent-starter
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_FRONTEND_DIST = _PROJECT_ROOT / "frontend" / "dist"

if _FRONTEND_DIST.exists():
    # Wenn frontend/dist existiert, liefere es unter "/" aus.
    app.mount("/", StaticFiles(directory=str(_FRONTEND_DIST), html=True), name="static")
else:
    # Andernfalls: Redirect von "/" auf die API-Doku
    @app.get("/")
    async def _root_redirect():
        return RedirectResponse(url="/docs", status_code=307)
