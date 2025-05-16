---
sidebar_position: 1
---

# Tests ausführen

Für die Komponenten der Anwendung wurden Tests geschrieben, um deren Qualität zu garantieren. Diese Tests befinden sich im Ordner `tests`.

## Installation der Dependencies

Um die Tests auszuführen werden folgende Dependencies benötigt:

- `pytest`
- `httpx`

Öffnen Sie ein Terminal und führen Sie folgende Befehle aus:

```bash
pip install pytest==8.3.3
```

sowie 

```bash
pip install httpx==0.27.2
```

## Ausführung

Öffnen Sie ein Terminal im Ordner `code` und führen Sie folgenden Befehl aus:

```bash
pytest
```

Alle verfügbaren Tests sollten automatisch ausgeführt werden. Wenn Sie einen Überblick haben möchten, können Sie sich die Testdateien auch ansehen. Jede Testdatei enthält Kommentare, die beschreiben, welche Komponente getestet wird.