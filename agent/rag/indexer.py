from __future__ import annotations
from pathlib import Path
from typing import List, Tuple
import json

from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer
import faiss

from agent.rag.utils import chunk_text, Chunk

STORE_DIR = Path(__file__).resolve().parent / "store"
INDEX_PATH = STORE_DIR / "index.faiss"
META_PATH = STORE_DIR / "meta.jsonl"
MODEL_PATH = STORE_DIR / "model.txt"


def _load_pdfs(pdf_dir: Path) -> List[Tuple[str, str]]:
    """Liest alle PDFs und gibt (filename, full_text) zurück."""
    items: List[Tuple[str, str]] = []
    for pdf in sorted(pdf_dir.glob("*.pdf")):
        try:
            text = extract_text(str(pdf))
        except Exception as e:
            print(f"[WARN] Konnte {pdf.name} nicht lesen: {e}")
            continue
        items.append((pdf.name, text))
    return items


def build_index(pdf_dir: str, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
    pdf_base = Path(pdf_dir)
    if not pdf_base.exists():
        raise FileNotFoundError(f"Ordner nicht gefunden: {pdf_dir}")

    STORE_DIR.mkdir(parents=True, exist_ok=True)

    docs: List[Chunk] = []
    for fname, text in _load_pdfs(pdf_base):
        chunks = chunk_text(text, source=fname, target_chars=1200, overlap=150)
        docs.extend(chunks)

    if not docs:
        raise RuntimeError("Keine Texte gefunden – liegen PDFs im angegebenen Ordner?")

    print(f"[INFO] Erzeuge Embeddings für {len(docs)} Chunks…")
    model = SentenceTransformer(model_name)
    embeddings = model.encode([d.text for d in docs], show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)

    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)  # Inner Product (mit normalisierten Vektoren = Cosine Sim)
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))
    with META_PATH.open("w", encoding="utf-8") as f:
        for d_ in docs:
            f.write(json.dumps({
                "source": d_.source,
                "chunk_id": d_.chunk_id,
                "text": d_.text
            }, ensure_ascii=False) + "\n")
    MODEL_PATH.write_text(model_name, encoding="utf-8")

    print(f"[OK] Index gespeichert: {INDEX_PATH}")
    print(f"[OK] Metadaten gespeichert: {META_PATH}")
