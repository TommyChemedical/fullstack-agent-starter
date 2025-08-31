from agent.tools.run import run


def test_allowed_python():
    res = run(["python", "-c", "print(42)"])
    assert res["code"] == 0
    assert "42" in res["stdout"]


def test_blocked_rm():
    res = run(["bash", "-lc", "rm -rf /"])
    assert res["code"] == 126
    assert "blocked" in res["stderr"]
