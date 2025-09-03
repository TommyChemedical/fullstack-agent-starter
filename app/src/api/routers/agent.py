from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from agent.tools.run import run
from agent.tools.pr import open_pull_request

router = APIRouter(prefix="/api/agent", tags=["agent"])

class ExecRequest(BaseModel):
    cmd: str
    timeout: Optional[int] = None

@router.post("/execute")
async def execute(req: ExecRequest) -> dict:
    return run(["bash", "-lc", req.cmd], timeout=req.timeout)

@router.get("/git/branch")
async def git_branch() -> dict:
    res = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if str(res.get("code")) != "0":
        raise HTTPException(status_code=500, detail=res.get("stderr") or "git error")
    return {"branch": (res.get("stdout") or "").strip()}

class PROpen(BaseModel):
    title: str
    body: str
    base: str = "main"

@router.post("/pr/open")
async def pr_open(payload: PROpen) -> dict:
    try:
        pr = open_pull_request(title=payload.title, body=payload.body, base=payload.base)
        return {"number": pr.get("number"), "url": pr.get("html_url")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
