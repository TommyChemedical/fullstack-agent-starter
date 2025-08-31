from __future__ import annotations
from pathlib import Path
from typing import List, Dict
import json

import faiss
from sentence_transformers import SentenceTransformer

STORE_DIR = Path(__file__).resolve().parent / "store"
INDEX_PATH = STORE_DIR / "index.faiss"
META_PATH = STORE_DIR / "meta.jsonl"
MODEL_PATH = STORE_DIR / "model.txt"


def _load_meta() -> List[Dict]:
    items: List[Dict] = []
    with META_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))
    return items


def search(query: str, top_k: int = 5) -> List[Dict]:
    if not INDEX_PATH.exists():
        raise FileNotFoundError("Kein Index gefunden – bitte zuerst indizieren (cli_rag.py index)")

    model_name = MODEL_PATH.read_text(encoding="utf-8").strip()
    model = SentenceTransformer(model_name)

    index = faiss.read_index(str(INDEX_PATH))
    meta = _load_meta()

    q_vec = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    D, I = index.search(q_vec, top_k)  # D: Scores, I: Indexe

    out: List[Dict] = []
    for rank, (score, idx) in enumerate(zip(D[0].tolist(), I[0].tolist()), start=1):
        if idx == -1:
            continue
        m = meta[idx]
        out.append({
            "rank": rank,
            "score": float(score),
            "source": m["source"],
            "chunk_id": m["chunk_id"],
            "text": m["text"]
        })
    return out


def pretty(results: List[Dict]) -> str:
    lines = []
    for r in results:
        lines.append(f"#{r['rank']} [{r['score']:.3f}] {r['source']} (chunk {r['chunk_id']})\n{r['text'][:400]}…\n")
    return "\n".join(lines)
