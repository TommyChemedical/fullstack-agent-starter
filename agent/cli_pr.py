import typer, json
from agent.tools.pr import open_pull_request

app = typer.Typer(help="PR-CLI")

@app.command()
def open(title: str = "feat: change by agent", body: str = "Automated PR"):
    pr = open_pull_request(title=title, body=body, base="main")
    print(json.dumps({"url": pr.get("html_url"), "number": pr.get("number")}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    app()
