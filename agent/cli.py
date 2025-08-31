import json
import shlex
import typer
from agent.tools import fs
from agent.tools.run import run
from agent.tools.git import git_create_branch, git_commit

app = typer.Typer(help="Mini-CLI zum Ausprobieren der Agent-Tools")

@app.command()
def read(path: str):
    """Datei anzeigen."""
    print(fs.read_file(path))

@app.command("write")
def write_cmd(path: str, content: str):
    """Datei schreiben."""
    fs.write_file(path, content)
    print("OK")

@app.command()
def execute(cmd: str):
    """Befehl ausführen, z. B.: execute "python -c \"print(42)\""""
    # Wichtig: shlex.split versteht Anführungszeichen korrekt
    res = run(shlex.split(cmd))
    print(json.dumps(res, ensure_ascii=False, indent=2))

@app.command()
def branch(name: str):
    print("OK" if git_create_branch(name) else "FEHLER")

@app.command()
def commit(message: str):
    print("OK" if git_commit(message) else "FEHLER")

if __name__ == "__main__":
    app()
