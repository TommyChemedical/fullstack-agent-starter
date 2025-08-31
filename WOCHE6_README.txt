Woche 6 – PR-Automation, Preview-Deploy, Test-Report

1) PR Checks aktivieren
- Kopiere .github/workflows/pr-summary.yml und .github/scripts/pr_summary.py ins Repo (gleiche Ordnerstruktur).
- Commit & push -> auf Pull Requests erstellt die Action automatisch einen Kommentar mit Test-Status und lädt ein HTML-Reporting als Artifact hoch.

2) Render PR-Previews (optional, empfohlen)
- 'render.yaml' ins Repo-Root legen, dann auf https://dashboard.render.com -> New -> Blueprint -> Repo verbinden -> Previews aktivieren.

3) PR direkt aus dem Terminal öffnen
- Dateien agent/tools/pr.py und agent/cli_pr.py ins Repo kopieren.
- Token setzen: export GH_TOKEN=ghp_xxx (Personal Access Token mit 'repo' Recht).
- Branch anlegen, committen, pushen, dann: python -m agent.cli_pr open --title "w6: demo"

4) Nützlich:
- Tests lokal: python -m pytest -q app
