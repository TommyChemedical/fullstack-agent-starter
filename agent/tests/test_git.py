from pathlib import Path
from agent.tools.run import run
from agent.tools.git import git_commit


def test_git_commit(tmp_path):
    # Neues Repo im Temp-Verzeichnis anlegen
    run(["git", "init"], cwd=str(tmp_path))
    p = tmp_path / "demo.txt"
    p.write_text("hello", encoding="utf-8")
    run(["git", "add", "demo.txt"], cwd=str(tmp_path))
    res = run(["git", "commit", "-m", "test"], cwd=str(tmp_path))
    assert res["code"] == 0
