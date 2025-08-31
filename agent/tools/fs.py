from pathlib import Path
from typing import List
from agent.tools.security import safe_join


def read_file(path: str) -> str:
    p = safe_join(path)
    return Path(p).read_text(encoding="utf-8")


def write_file(path: str, content: str) -> None:
    p = safe_join(path)
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(content, encoding="utf-8")


def list_dir(path: str, pattern: str = "*") -> List[str]:
    p = safe_join(path)
    return [str(x) for x in Path(p).glob(pattern)]
