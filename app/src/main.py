from fastapi import FastAPI
from app.src.api.routers.courses import router as courses_router

app = FastAPI(title="EdTech Backend", version="0.1.0")

@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "version": "0.1.0", "agent": "ready"}

# API-Router registrieren
app.include_router(courses_router)
