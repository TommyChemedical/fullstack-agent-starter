from agent.rag.utils import chunk_text


def test_chunking_basic():
    txt = ("Kapitel 1\n\n" + "A "*1000 + "\n\nKapitel 2\n\n" + "B "*1000)
    chunks = chunk_text(txt, source="demo.pdf", target_chars=600, overlap=100)
    assert len(chunks) >= 3
    assert chunks[0].source == "demo.pdf"
    assert chunks[0].text
