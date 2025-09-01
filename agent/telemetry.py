from __future__ import annotations
from typing import Dict, Any, Iterable
from pathlib import Path
import json, time
from agent.config import load as load_cfg


def _ensure_dir() -> Path:
    cfg = load_cfg()
    tel = cfg.get("telemetry", {})
    d = Path(tel.get("dir", "workspaces/telemetry")).resolve()
    d.mkdir(parents=True, exist_ok=True)
    return d


def record_event(kind: str, payload: Dict[str, Any]) -> None:
    d = _ensure_dir()
    row = {"ts": int(time.time()*1000), "kind": kind, **payload}
    with open(d / "events.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def summarize() -> Dict[str, Any]:
    d = _ensure_dir()
    path = d / "events.jsonl"
    stats = {"total": 0, "by_kind": {}, "http": {"count": 0, "avg_ms": 0.0}}
    if not path.exists():
        return stats
    lat_sum = 0.0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stats["total"] += 1
            try:
                obj = json.loads(line)
            except Exception:
                continue
            k = obj.get("kind")
            stats["by_kind"][k] = stats["by_kind"].get(k, 0) + 1
            if k == "http":
                stats["http"]["count"] += 1
                lat_sum += float(obj.get("duration_ms", 0))
    if stats["http"]["count"]:
        stats["http"]["avg_ms"] = round(lat_sum / stats["http"]["count"], 2)
    return stats
