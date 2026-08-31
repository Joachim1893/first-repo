# Implementierungsplan: Einfaches Snake-Spiel (HTML5 / JS)

Entwurf und Architektur für ein schnelles, leichtgewichtiges und barrierefreies Snake-Spiel im Browser, das direkt ohne externe Abhängigkeiten in einer einzigen HTML/JS-Datei umgesetzt werden kann.

---

## User Review Required

> [!IMPORTANT]
> **Technologie-Wahl**: Es wird ein **HTML5 Canvas + Plain JavaScript** Ansatz vorgeschlagen. Dies ermöglicht das Ausführen des Spiels in jedem Browser ohne Build-Schritte oder Webserver.
>
> **Standard-Konfiguration**:
> * **Spielfeldgröße**: 20 x 20 Rasterzellen (Rasterzellengröße: 20px, Spielfeld: 400x400px).
> * **Standard-Wand-Modus**: Tödliche Wände (Classic Mode), umschaltbar auf Durchgleiten (Wrap-Around).
> * **Farbschema**: Neon-Grün (`#00FF66`) für die Schlange, Dunkler Hintergrund (`#1A1A1A`), Apfel-Rot (`#FF4444`) mit dezenter Kreis-Form für das Futter.

---

## Open Questions

> [!NOTE]
> 1. **Steuerungs-Optionen**: Sollen neben den Pfeiltasten auch `WASD`-Tasten unterstützt werden? (Im Entwurf: Ja, beide werden unterstützt).
> 2. **Audio/Sound-Effekte**: Soll das Spiel einfache Soundeffekte (Web Audio API synthetisierte Beeps beim Fressen/Game Over) enthalten?

---

## Proposed Changes

Das gesamte Spiel wird im Projektordner `C:\000_Vibe_Arnie\016_Antigravity` als saubere und erweiterbare Web-Applikation angelegt.

### Web Application Component

#### [NEW] [index.html](file:///C:/000_Vibe_Arnie/016_Antigravity/index.html)
* **HTML-Struktur**:
  * Canvas-Element (400x400px) für das Spielfeld.
  * Scoreboard (Aktueller Score & Highscore).
  * Steuerungs- & Einstellungs-Panel (Modus-Umschalter für Wand-Mechanik: *Tödlich* vs. *Wrap-Around*, Start/Pause-Buttons).
  * Hilfetext für Steuerung (`Pfeiltasten` / `WASD` zum Bewegen, `Leertaste` für Pause).

#### [NEW] [style.css](file:///C:/000_Vibe_Arnie/016_Antigravity/style.css)
* Retro-Modernes Design mit dunklem Theme.
* Hoher Kontrast für gute Lesbarkeit.
* Zentenriertes Layout für Canvas und Steuerungs-Elemente.

#### [NEW] [game.js](file:///C:/000_Vibe_Arnie/016_Antigravity/game.js)
* **Grid-System & Loop**: `requestAnimationFrame` mit festem Tick-Intervall (z.B. 100ms) und Geschwindigkeits-Skalierung.
* **Input-Buffer Queue**: Speichert bis zu 2 gepufferte Tastendrücke, um instantane 180°-Eigenkollisionen zu verhindern.
* **Spiellogik & Kollision**:
  * Bewegung der Schlange (Array von `{x, y}`-Koordinaten).
  * Kollisionsprüfung mit Körper und Wänden (je nach ausgewähltem Modus).
  * Futter-Spawning-Logik (Filtert besetzte Grid-Felder aus).
* **Game State Management**: Zustände `IDLE`, `RUNNING`, `PAUSED`, `GAME_OVER`. Speicheranbindung an `localStorage` für Highscores.

---

## Verification Plan

### Automated Tests
* Manuelle Überprüfung der JavaScript-Syntax und Ausführung in einer lokalen Browser-Umgebung oder per HTML-Testlauf.

### Manual Verification
1. **Wand-Modi testen**:
   * *Tödlicher Modus*: Gegen die Wand fahren -> *Game Over* muss auslösen.
   * *Wrap-Around Modus*: Gegen die Wand fahren -> Schlange muss an der gegenüberliegenden Seite wieder auftauchen.
2. **Input-Buffering testen**:
   * Schnell `Rechts` + `Unten` drücken, während die Schlange nach oben fährt. Die Schlange muss erst nach rechts, dann nach unten abbiegen, ohne sich sofort selbst zu fressen.
3. **Futter-Spawning testen**:
   * Prüfen, ob das Futter niemals auf dem Schlangenkörper gespawnt wird.
4. **Highscore & Pause**:
   * Spiel pausieren mit `Leertaste`.
   * Highscore-Aktualisierung im `localStorage` verifizieren.
