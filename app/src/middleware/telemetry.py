from __future__ import annotations
import time
from starlette.middleware.base import BaseHTTPMiddleware
from agent.telemetry import record_event

class TelemetryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        t0 = time.time()
        resp = await call_next(request)
        dur = int((time.time() - t0) * 1000)
        try:
            record_event("http", {
                "path": request.url.path,
                "method": request.method,
                "status": resp.status_code,
                "duration_ms": dur,
            })
        except Exception:
            pass
        return resp
