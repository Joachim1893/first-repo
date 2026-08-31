# Implementierungsplan: Python Snake-Spiel mit Tkinter GUI

Entwurf und Architektur für ein plattformübergreifendes, abhängigkeitsfreies Python Snake-Spiel mit grafischer Benutzeroberfläche (GUI) auf Basis der Standard-Bibliothek `tkinter`.

---

## User Review Required

> [!IMPORTANT]
> **GUI-Framework**: Es wird **`tkinter`** (Bestandteil der Python Standard-Bibliothek) verwendet. Es sind **keine externen Pakete** (wie `pygame`) erforderlich. Das Spiel kann direkt mit `python snake.py` gestartet werden.
>
> **Standard-Konfiguration**:
> * **Spielfeld**: 400x400 Pixel (20x20 Raster, 20px Zellengröße).
> * **Farben**: Neon-Grün (`#00FF66`) für die Schlange, Dunkles Theme (`#1A1A1A`), Apfel-Rot (`#FF4444`) für das Futter.
> * **Wand-Mechanik**: Option wählbar zwischen *Tödlich* (Classic) und *Durchgleiten* (Wrap-Around).

---

## Open Questions

> [!NOTE]
> 1. **Highscore-Speicherung**: Der Highscore wird lokal in einer Datei `highscore.txt` im Projektordner gespeichert.
> 2. **Steuerung**: Pfeiltasten und `WASD`-Tasten werden unterstützt, `Leertaste` steuert die Pause.

---

## Proposed Changes

Das Spiel wird als saubere, objektorientierte Python-Anwendung im Projektordner `C:\000_Vibe_Arnie\016_Antigravity` erstellt.

### Python GUI Application Component

#### [NEW] [snake.py](file:///C:/000_Vibe_Arnie/016_Antigravity/snake.py)
* **GUI-Aufbau (Tkinter)**:
  * Hauptfenster mit dunklem Farbschema.
  * `tk.Canvas` (400x400px) für die Grafik-Ausgabe.
  * Scoreboard (`tk.Label`) für aktuellen Score und Highscore.
  * Steuerungsleiste (`ttk.Combobox` für Wand-Modus, `ttk.Button` für Start/Pause).
* **Spiellogik**:
  * Klasse `SnakeGame` kapselt den kompletten Spielzustand.
  * Grid-basierte Bewegung mit `root.after()` Tick-Loop.
  * **Input-Buffer Queue**: Speichert Richtungsentscheidungen und blockiert instantane 180°-Eigenkollisionen.
  * Kollisionsprüfung für Wände (Tödlich vs. Wrap-Around) und den Schlangenkörper.
  * Zufälliges Futter-Spawning auf freien Rasterfeldern.
  * Geschwindigkeitssteigerung bei steigendem Score.

---

## Verification Plan

### Automated Tests
* Ausführung eines Syntax- & Import-Checks mit Python:
  ```powershell
  python -m py_compile snake.py
  ```

### Manual Verification
1. **Spielstart & GUI**:
   * Spiel mit `python snake.py` starten und prüfen, ob das Tkinter-Fenster ordnungsgemäß öffnet.
2. **Wand-Modi**:
   * *Tödlicher Modus*: Gegen Wand fahren löst Game Over aus.
   * *Wrap-Around Modus*: Schlange erscheint auf der anderen Seite.
3. **Steuerung & Input Buffer**:
   * Schnelles Drücken zweier Richtungen prüfen.
4. **Highscore**:
   * Prüfen, ob `highscore.txt` angelegt und aktualisiert wird.
