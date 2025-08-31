from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re


@dataclass
class Chunk:
    text: str
    source: str  # z. B. Dateiname
    chunk_id: int


def normalize_whitespace(text: str) -> str:
    text = text.replace("\u00a0", " ")  # NBSP
    text = re.sub(r"[\t\r]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, source: str, target_chars: int = 1200, overlap: int = 150) -> List[Chunk]:
    """Einfache, robuste Chunking-Strategie über Zeichenlänge.
    - target_chars ~ entspricht grob 200–300 Wörtern
    - overlap hält Kontext zwischen Chunks
    """
    text = normalize_whitespace(text)
    if not text:
        return []
    chunks: List[Chunk] = []
    start = 0
    cid = 0
    while start < len(text):
        end = min(len(text), start + target_chars)
        # versuche, am Absatzende zu schneiden
        slice_ = text[start:end]
        last_break = slice_.rfind("\n\n")
        if last_break != -1 and end - start > 400:
            end = start + last_break
        chunk_text_ = text[start:end].strip()
        if chunk_text_:
            chunks.append(Chunk(text=chunk_text_, source=source, chunk_id=cid))
            cid += 1
        # nächsten Start inkl. Überlappung berechnen
        start = end - overlap
        if start < 0:
            start = 0
        if start >= len(text):
            break
        # bei sehr kleinen Resten abbrechen
        if end >= len(text):
            break
    return chunks
