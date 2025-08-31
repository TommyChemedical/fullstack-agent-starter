import re
from pathlib import Path
from typing import Tuple
from agent.config import PROJECT_ROOT

SECRET_REGEX = re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*([^\s]+)")


def redact(text: str) -> str:
    """Ersetzt offensichtliche Geheimnisse in Texten durch ****."""
    def repl(m: re.Match) -> str:
        prefix = m.group(0).split(m.group(2))[0]
        return prefix + "****"
    return SECRET_REGEX.sub(repl, text or "")


def safe_join(path: str) -> Path:
    """Erzwingt, dass Pfade **unterhalb** des Projektordners liegen (kein ".." nach oben)."""
    p = (PROJECT_ROOT / path).resolve()
    if not str(p).startswith(str(PROJECT_ROOT.resolve())):
        raise ValueError("Pfad liegt außerhalb des Projektordners")
    return p
