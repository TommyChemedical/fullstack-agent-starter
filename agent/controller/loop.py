from __future__ import annotations
from pathlib import Path
from typing import Optional
from loguru import logger

from agent.tools import fs
from agent.tools.git import git_create_branch, git_commit
from agent.tools.run import run

# Optional: RAG nutzen, wenn Index existiert
try:
    from agent.rag.search import search
except Exception:  # pragma: no cover
    search = None  # type: ignore


ROOT = Path(__file__).resolve().parents[2]
APP_MAIN = ROOT / "app/src/main.py"
APP_TEST = ROOT / "app/tests/test_health.py"


def _add_agent_field_to_health() -> bool:
    """Erweitert den Health‑Endpoint um "agent": "ready". Idempotent."""
    text = fs.read_file(str(APP_MAIN))
    if '"agent": "ready"' in text:
        return False  # schon vorhanden

    # einfache, robuste Ersetzung
    needle = 'return {"status": "ok", "version": "0.1.0"}'
    repl = 'return {"status": "ok", "version": "0.1.0", "agent": "ready"}'
    if needle in text:
        new = text.replace(needle, repl)
    else:
        # Fallback: suche die Zeile mit `return {` und füge agent hinzu
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if line.strip().startswith("return {"):
                if line.strip().endswith("}"):
                    line = line.rstrip("}\n").rstrip()  # entferne schließende Klammer
                    if not line.endswith(","):
                        line += ","
                    line += ' "agent": "ready" }'
                    lines[i] = line
                    break
        new = "\n".join(lines)

    fs.write_file(str(APP_MAIN), new)
    return True


def _ensure_test_checks_agent() -> bool:
    """Ergänzt im Test die Prüfung auf das neue Feld. Idempotent."""
    t = fs.read_file(str(APP_TEST))
    if 'data.get("agent") == "ready"' in t:
        return False
    # Füge unter die bestehende Status‑Prüfung eine neue Zeile ein
    lines = t.splitlines()
    for i, line in enumerate(lines):
        if "assert data.get(\"status\") == \"ok\"" in line or "assert data.get('status') == 'ok'" in line:
            indent = line[: len(line) - len(line.lstrip())]
            lines.insert(i + 1, f"{indent}assert data.get(\"agent\") == \"ready\"")
            break
    new = "\n".join(lines)
    fs.write_file(str(APP_TEST), new)
    return True


def _rag_snippets() -> str:
    if search is None:
        return "(RAG nicht eingerichtet – überspringe Zitate)"
    try:
        hits = search("Walking Skeleton / Tracer Bullet Prinzip (Pragmatic Programmer)", top_k=3)
        out = []
        for h in hits:
            out.append(f"- {h['source']} (Score {h['score']:.3f}) – Auszug: {h['text'][:200]}…")
        return "\n".join(out) if out else "(Keine Treffer)"
    except Exception as e:  # robust bleiben
        return f"(RAG-Suche fehlgeschlagen: {e})"


def run_walking_skeleton_health(dry_run: bool = False) -> int:
    """Kleiner End‑to‑End‑Task: Health erweitern, Test ergänzen, Tests laufen lassen, committen."""
    logger.info("Plan: Health‑Endpoint um Feld 'agent' erweitern; Test anpassen; Tests ausführen; Commit.")
    logger.info("Begründung/Zitate:\n" + _rag_snippets())

    # 1) Branch
    branch_name = "feat/w4-health-agent"
    ok = git_create_branch(branch_name)
    logger.info(f"Branch {branch_name}: {'OK' if ok else 'bereits vorhanden oder Fehler – fahre fort'}")

    changed_any = False

    # 2) Code ändern
    changed = _add_agent_field_to_health()
    logger.info(f"Health‑Endpoint geändert: {'JA' if changed else 'NEIN (war schon so)'}")
    changed_any = changed_any or changed

    # 3) Test anpassen
    changed_t = _ensure_test_checks_agent()
    logger.info(f"Test ergänzt: {'JA' if changed_t else 'NEIN (war schon so)'}")
    changed_any = changed_any or changed_t

    # 4) Lint/Tests
    # (Lint optional – wir konzentrieren uns auf Tests)
    res = run(["python", "-m", "pytest", "-q", "app"])
    logger.info(f"Tests: exit={res['code']} duration={res['duration_ms']}ms")
    if res["stdout"]:
        logger.info("Tests stdout:\n" + res["stdout"])
    if res["stderr"]:
        logger.warning("Tests stderr:\n" + res["stderr"])

    if res["code"] != 0:
        logger.error("Tests fehlgeschlagen – bitte Ausgabe ansehen und ggf. zurücksetzen.")
        return res["code"]

    # 5) Commit
    if changed_any:
        okc = git_commit("w4: extend /health with agent=ready + test")
        logger.info(f"Commit: {'OK' if okc else 'NICHTS ZU COMMITTEN'}")
    else:
        logger.info("Keine Änderungen – nichts zu committen.")

    logger.info("Walking Skeleton abgeschlossen. (PR‑Erstellung/Preview folgt in Woche 6)")
    return 0
