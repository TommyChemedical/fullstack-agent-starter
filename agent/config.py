from __future__ import annotations
from typing import Any, Dict
import os
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS: Dict[str, Any] = {
    "telemetry": {
        "enabled": True,
        "dir": str(ROOT / "workspaces" / "telemetry"),
    },
    "exec": {
        "cwd": str(ROOT / "workspaces"),
        "timeout_sec": 180,
        "allowed_bins": ["python", "pytest", "uvicorn", "bash", "sh"],
        "block_patterns": [
            "rm -rf /", "mkfs", "dd if=", ":(){:|:&};:", "shutdown", "reboot",
            "chmod 777 -R /", "chown -R /", "/dev/sd", ">/dev/",
        ],
        "block_net": True,
    },
}

YAML_PATH = ROOT / "config" / "settings.yaml"


def load() -> Dict[str, Any]:
    cfg = DEFAULTS.copy()
    if YAML_PATH.exists():
        with open(YAML_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        # flache, vorsichtige Merge-Strategie
        for k, v in data.items():
            if isinstance(v, dict) and isinstance(cfg.get(k), dict):
                cfg[k].update(v)  # type: ignore
            else:
                cfg[k] = v
    # Env-Override
    tel_on = os.getenv("TELEMETRY_ENABLED")
    if tel_on is not None:
        cfg["telemetry"]["enabled"] = tel_on.strip() not in ("0", "false", "False")
    return cfg
