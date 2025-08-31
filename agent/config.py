from pathlib import Path

# Wurzel des Projekts: Standard = aktuelles Verzeichnis, in dem du arbeitest.
# Du kannst das bei Bedarf anpassen.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Maximal erlaubte Größe für Ausgaben (Schutz vor Log-Fluten)
STDIO_LIMIT = 4000  # Zeichen

# Erlaubte Programme (erste "Wort" des Befehls)
ALLOWED_BINARIES = {
    "python", "pip", "pytest", "uvicorn", "git", "bash", "sh"
}

# Problematische Muster – solche Befehle blocken wir hart.
BLOCK_PATTERNS = [
    "rm -rf /",  # gefährlich
    ">/dev/sda",  # platzhalterisch
    "curl http", "wget http",  # willkürliches Netz (später gezielt erlauben)
]
