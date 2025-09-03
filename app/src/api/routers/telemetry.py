from fastapi import APIRouter
from agent.telemetry import summarize

router = APIRouter(prefix="/api/telemetry", tags=["telemetry"])

@router.get("/summary")
async def telemetry_summary() -> dict:
    return summarize()
