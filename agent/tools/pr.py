import os, re, json
import httpx
from .run import run

def _get_current_branch() -> str:
    res = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if res["code"] != 0: raise RuntimeError("git branch not found")
    return res["stdout"].strip()

def _get_origin_repo() -> tuple[str, str]:
    res = run(["git", "remote", "get-url", "origin"])
    if res["code"] != 0: raise RuntimeError("no git origin remote")
    url = res["stdout"].strip()
    m = re.search(r"github.com[:/](?P<owner>[^/]+)/(?P<repo>[^\.\s]+)", url)
    if not m: raise RuntimeError("cannot parse GitHub repo from origin URL")
    return m.group("owner"), m.group("repo")

def open_pull_request(title: str, body: str, base: str = "main") -> dict:
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token: raise RuntimeError("Set GH_TOKEN or GITHUB_TOKEN in env")
    head = _get_current_branch()
    owner, repo = _get_origin_repo()
    api = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    payload = {"title": title, "body": body, "head": head, "base": base}
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    r = httpx.post(api, headers=headers, json=payload, timeout=30)
    if r.status_code >= 300:
        raise RuntimeError(f"PR create failed: {r.status_code} {r.text}")
    return r.json()
