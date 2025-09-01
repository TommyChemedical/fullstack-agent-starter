from __future__ import annotations
from typing import Dict, Tuple
import os
import re
import httpx

from agent.tools.run import run


def _ok(res: Dict[str, str]) -> bool:
    """Returncode '0' als Erfolg werten (run() liefert Strings)."""
    try:
        return int(str(res.get("code", "1"))) == 0
    except Exception:
        return False


def _get_current_branch() -> str:
    res = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if not _ok(res):
        raise RuntimeError("git branch not found")
    return (res.get("stdout") or "").strip()


def _get_origin_repo() -> Tuple[str, str]:
    """Liest owner/repo aus dem 'origin'-Remote (SSH oder HTTPS)."""
    res = run(["git", "remote", "get-url", "origin"])
    if not _ok(res):
        raise RuntimeError("git origin not found")
    url = (res.get("stdout") or "").strip()

    # Beispiele:
    # git@github.com:Owner/Repo.git
    # https://github.com/Owner/Repo.git
    # https://github.com/Owner/Repo
    m = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$", url, re.IGNORECASE)
    if not m:
        raise RuntimeError(f"cannot parse origin url: {url}")
    owner = m.group("owner")
    repo = m.group("repo")
    return owner, repo


def open_pull_request(title: str, body: str, base: str = "main") -> dict:
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Set GH_TOKEN or GITHUB_TOKEN in env")

    head = _get_current_branch()
    owner, repo = _get_origin_repo()
    api = f"https://api.github.com/repos/{owner}/{repo}/pulls"

    payload = {"title": title, "body": body, "head": head, "base": base}
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    r = httpx.post(api, headers=headers, json=payload, timeout=30)
    if r.status_code >= 300:
        raise RuntimeError(f"PR create failed: {r.status_code} {r.text}")
    return r.json()
