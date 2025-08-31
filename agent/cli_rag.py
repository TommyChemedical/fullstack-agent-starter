import typer
from agent.rag.indexer import build_index
from agent.rag.search import search, pretty

app = typer.Typer(help="RAG-CLI: PDF-Indexierung & Suche")

@app.command()
def index(pdf_dir: str = typer.Argument("knowledge/pdfs")):
    build_index(pdf_dir)

@app.command()
def query(q: str, k: int = 5):
    res = search(q, top_k=k)
    print(pretty(res))

if __name__ == "__main__":
    app()
