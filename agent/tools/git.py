from agent.tools.run import run


def git_create_branch(name: str) -> bool:
    res = run(["git", "checkout", "-b", name])
    return res["code"] == 0


def git_commit(message: str) -> bool:
    add = run(["git", "add", "-A"])
    if add["code"] != 0:
        return False
    commit = run(["git", "commit", "-m", message])
    return commit["code"] == 0
