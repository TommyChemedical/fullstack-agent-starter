CHECKLIST = [
    "Änderung klein & rücksetzbar (kein Big Bang)",
    "Tests angepasst oder ergänzt",
    "Keine Secrets im Code/Logs",
    "Benennung klar (branch, commit message)",
    "Build/Tests lokal grün",
]

def as_text() -> str:
    return "\n".join(f"- {item}" for item in CHECKLIST)
