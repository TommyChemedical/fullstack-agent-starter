from agent.tools.run import run


def test_blocks_rm_rf_root():
    res = run(["bash", "-lc", "rm -rf /"])
    assert res["code"] == "2"
    assert "blocked pattern" in res["stderr"]


def test_blocks_network():
    res = run(["bash", "-lc", "curl -sS https://example.com"])
    assert res["code"] == "2"
    assert "network" in res["stderr"]


def test_allows_python_eval():
    res = run(["python", "-c", "print(40+2)"])
    assert res["code"] == "0"
    assert res["stdout"].strip() == "42"


def test_timeout_short():
    res = run(["bash", "-lc", "python -c 'import time; time.sleep(1)'"], timeout=0)
    assert res["code"] in ("124", "2")  # je nach Policy timeout/block
