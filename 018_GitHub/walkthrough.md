# Walkthrough: Snake-Spiel Implementierung (HTML5 & Python GUI)

Das klassische Snake-Spiel wurde erfolgreich sowohl als **HTML5/JS Web-Anwendung** als auch als **Python GUI-Anwendung (Tkinter)** im Projektordner `C:\000_Vibe_Arnie\016_Antigravity` umgesetzt.

---

## Erstellte Komponenten

### 1. Python GUI-Variante: [snake.py](file:///C:/000_Vibe_Arnie/016_Antigravity/snake.py)
* **Technologie:** Native `tkinter` Standard-Bibliothek (kein `pip install` nötig).
* **Funktionen:**
  * Grafisches Tkinter Canvas (400x400px).
  * Wandmechanik wählbar über Dropdown (*Tödlich* vs. *Wrap-Around*).
  * Input-Buffering Queue zur Vermeidung von 180°-Eigenkollisionsfehlern.
  * Speicherung des Highscores in der lokalen Datei `highscore.txt`.
  * Ausführbar mit: `python snake.py`.

### 2. Web-Variante: [index.html](file:///C:/000_Vibe_Arnie/016_Antigravity/index.html)
* **[style.css](file:///C:/000_Vibe_Arnie/016_Antigravity/style.css):** Retro-Modernes Dark Theme mit Neon-Grün Akzenten.
* **[game.js](file:///C:/000_Vibe_Arnie/016_Antigravity/game.js):** Canvas Engine, Input Buffering, Highscore in `localStorage`.
* Ausführbar per Doppelklick in jedem Webbrowser.

---

## Verifizierung & Tests

| Testfall | Erwartetes Verhalten | Ergebnis |
| :--- | :--- | :--- |
| **Python Syntax Check** | `python -m py_compile snake.py` schließt ohne Fehler ab | ✅ Code 0 |
| **Wandmodus "Tödlich"** | Schlange kollidiert mit der Wand -> Game Over | ✅ Erfolgreich |
| **Wandmodus "Wrap-Around"** | Schlange durchfährt die Wand und erscheint gegenüber | ✅ Erfolgreich |
| **Input Buffer** | Schnelles Drücken zweier Richtungen hintereinander blockiert Selbstmord | ✅ Erfolgreich |
| **Highscore Speicherung** | `highscore.txt` wird bei neuen Rekorden aktualisiert | ✅ Erfolgreich |

---

## Ausführung

* **Python GUI starten:**
  ```powershell
  python snake.py
  ```
* **HTML5 Web-Variante starten:**
  Öffne [index.html](file:///C:/000_Vibe_Arnie/016_Antigravity/index.html) im Browser.
