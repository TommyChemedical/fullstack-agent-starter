import pytest
from agent.tools.fs import write_file, read_file


def test_write_and_read(tmp_path, monkeypatch):
    # Schreibe in einen Unterordner des Projekts (simulieren wir relativ)
    rel = "workspaces/test.txt"
    write_file(rel, "hello")
    assert read_file(rel) == "hello"
