import typer
from agent.controller.loop import run_walking_skeleton_health
from agent.controller import self_review

app = typer.Typer(help="Aufgaben-CLI für den Controller")

@app.command()
def walking_skeleton_health():
    """Führt den kleinen End‑to‑End‑Task aus (Health erweitern + Test + Tests + Commit)."""
    code = run_walking_skeleton_health()
    print("Exit:", code)

@app.command()
def checklist():
    """Zeigt die Self‑Review‑Checkliste."""
    print(self_review.as_text())

if __name__ == "__main__":
    app()
