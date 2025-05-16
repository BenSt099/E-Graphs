---
sidebar_position: 1
---

# Installation der Dependencies

1. **Graphviz**

**Graphviz** ist eine Software, die zum Erzeugen von Graphen verwendet wird. Dazu gibt es viele weitere Features wie das Exportieren in unterschiedliche Dateiformate.

- [Graphviz herunterladen](https://graphviz.org/download/)

- Achten Sie während der Installation darauf, Graphviz zum PATH hinzuzufügen (siehe auch nächster Stichpunkt).

- **Windows** Falls Sie unter Windows arbeiten, achten Sie darauf, dass Sie das Programm `dot` vom Terminal aus aufrufen können. Überprüfbar ist das mit `dot --version`. Allgemein gibt es [hier](https://forum.graphviz.org/t/new-simplified-installation-procedure-on-windows/224) eine Anleitung für Windows.


2. **Python Pakete**

Die notwendigen Pakete finden Sie in der Datei `requirements.txt`. Öffnen Sie im selben Ordner ein Terminal und führen Sie folgenden Befehl aus:

```bash
pip install -r requirements.txt
```
