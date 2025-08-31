import shlex
import subprocess
import time
from typing import Dict, List, Union

from agent.config import ALLOWED_BINARIES, STDIO_LIMIT, BLOCK_PATTERNS
from agent.tools.security import redact


def _is_allowed(cmd: List[str]) -> bool:
    if not cmd:
        return False
    head = cmd[0]
    return head in ALLOWED_BINARIES


def _is_blocked(command_line: str) -> bool:
    lowered = command_line.lower()
    return any(pat in lowered for pat in BLOCK_PATTERNS)


def run(command: List[str], timeout: int = 180, cwd: str = ".") -> Dict[str, Union[str, int]]:
    """
    Führt **erlaubte** Befehle aus und schneidet Ausgaben auf eine sichere Länge.
    - command: z. B. ["python", "-c", "print(42)"]
    - timeout: Sekunden
    - cwd: Arbeitsverzeichnis
    Rückgabe: {code, stdout, stderr, duration_ms}
    """
    # Sicherheitschecks
    if not _is_allowed(command):
        return {"code": 126, "stdout": "", "stderr": f"command not allowed: {command[:1]}", "duration_ms": 0}

    cmdline = " ".join(shlex.quote(c) for c in command)
    if _is_blocked(cmdline):
        return {"code": 126, "stdout": "", "stderr": "blocked by policy", "duration_ms": 0}

    start = time.time()
    proc = subprocess.Popen(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        return {"code": 124, "stdout": "", "stderr": "timeout", "duration_ms": int((time.time()-start)*1000)}

    # Ausgaben begrenzen & Geheimnisse maskieren
    out = redact(out)[-STDIO_LIMIT:]
    err = redact(err)[-STDIO_LIMIT:]

    return {"code": proc.returncode, "stdout": out, "stderr": err, "duration_ms": int((time.time()-start)*1000)}
