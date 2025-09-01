from __future__ import annotations
from typing import Dict, List
import os, shlex, subprocess, time, re
from pathlib import Path

from agent.config import load as load_cfg

# Rückgabe-Typ bleibt ein einfaches Dict (3.9-kompatibel)

def run(command: List[str], timeout: int = None, cwd: str = None) -> Dict[str, str]:
    """
    Sichere Ausführung externer Kommandos.
    - Enforced CWD (workspaces)
    - Allowlist für Binaries, Blockliste für gefährliche Muster
    - Optionales Netzwerkverbot (primitive Heuristik)
    - Zeitlimit (0 bedeutet: sofortiger Timeout)
    """
    cfg = load_cfg()
    exec_cfg = cfg.get("exec", {})

    enforce_cwd = cwd if cwd is not None else exec_cfg.get("cwd")
    enforce_cwd = str(Path(enforce_cwd).resolve())
    os.makedirs(enforce_cwd, exist_ok=True)

    # Timeout korrekt behandeln: None = Default aus Config; 0 = sofortiger Timeout; <0 → 0
    if timeout is None:
        to = int(exec_cfg.get("timeout_sec", 180))
    else:
        try:
            to = max(0, int(timeout))
        except Exception:
            to = 0

    allowed = set(exec_cfg.get("allowed_bins", []))
    blocks = [re.compile(p) for p in exec_cfg.get("block_patterns", [])]
    block_net = bool(exec_cfg.get("block_net", True))

    # Kommando als String für Heuristiken (auch wenn Liste übergeben)
    cmd_str = " ".join(shlex.quote(c) for c in command)

    # 1) Binary-Allowlist prüfen (erstes Token)
    first = Path(command[0]).name
    if first not in allowed:
        return {"code": "2", "stdout": "", "stderr": f"binary not allowed: {first}", "duration_ms": "0"}

    # 2) Harte Blockmuster
    for rx in blocks:
        if rx.search(cmd_str):
            return {"code": "2", "stdout": "", "stderr": f"blocked pattern: {rx.pattern}", "duration_ms": "0"}

    # 3) Netzwerk grob untersagen (nur Heuristik)
    if block_net and ("http://" in cmd_str or "https://" in cmd_str or "curl" in cmd_str or "wget" in cmd_str):
        return {"code": "2", "stdout": "", "stderr": "network blocked by policy", "duration_ms": "0"}

    env = os.environ.copy()
    env.setdefault("PYTHONUNBUFFERED", "1")
    env.setdefault("TOKENIZERS_PARALLELISM", "false")

    start = time.time()
    try:
        proc = subprocess.run(
            command,
            cwd=enforce_cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=to,
            check=False,
        )
        dur = int((time.time() - start) * 1000)
        return {
            "code": str(proc.returncode),
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "duration_ms": str(dur),
        }
    except subprocess.TimeoutExpired:
        dur = int((time.time() - start) * 1000)
        return {"code": "124", "stdout": "", "stderr": "timeout", "duration_ms": str(dur)}
