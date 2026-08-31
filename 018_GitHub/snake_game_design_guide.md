# Snake Game: Design- & Entwicklungs-Leitfaden

Ein umfassender Überblick über Wand-Mechaniken, Farbgestaltung, Barrierefreiheit und die wichtigsten technischen Kernanforderungen für die Implementierung eines klassischen Snake-Spiels.

---

## 1. Wand-Mechanik: Tödliche Wände vs. Durchgleiten (Wrap-Around)

Die Entscheidung zwischen festen Wänden und einer durchlässigen Spielfeldbegrenzung verändert das Spielgefühl und die Strategie grundlegend.

| Kriterium | Tödliche Wände (*Die-on-Wall*) | Durch Wände gleiten (*Wrap-Around*) |
| :--- | :--- | :--- |
| **Hauptgefahr** | Wände + Eigenkollision | Nur Eigenkollision |
| **Nostalgie-Bezug** | Original Nokia *Snake* (1997) | Nokia *Snake II* (2000) |
| **Spielgefühl** | Nervenkitzel, hohe Präzision, Risikomanagement | Entspannt, flüssig, kontinuierlich |
| **Fokus** | Spielfeldränder & Ecken meiden | Körperlänge & Abschnitte auf dem Feld managen |
| **Zielgruppe** | Arcade-Fans, Hardcore-Gamer, Wettbewerb | Casual-Gamer, Anfänger |

> [!TIP]
> **Best Practice:** Biete beide Modi in den Einstellungen an! Verwende *Tödliche Wände* als Standard (*Default*) und erlaube Spielern, über eine Einstellung auf *Wrap-Around* umzuschalten.

---

## 2. Farbkonzept & Barrierefreiheit (UX & Accessibility)

* **Klassische Farbschemata:**
  * **Cyberpunk / Neon:** Helligkeitsstarkes Neon-Grün (`#00FF66`) auf sehr dunklem Hintergrund (`#1A1A1A`).
  * **Nokia LCD Retro:** Dunkelgrün (`#2D4018`) auf hellgrau-grünem LCD-Hintergrund (`#9BBC0F`).
* **Kontrast & Erkennbarkeit:**
  * Die Schlange muss sich zu jedem Zeitpunkt deutlich vom Hintergrund und vom Futter unterscheiden.
  * Das Futter benötigt eine kräftige Gegenfarbe (z. B. Rot oder Orange).
* **Barrierefreiheit (Sehschwächen):**
  * Vermeide reine Rot-Grün-Farbkodierungen ohne sekundäre Symbole.
  * Verwende Formen oder Icons (z. B. ein Apfel-Icon oder eine pulsierende Animate) für das Futter.

---

## 3. Die 3 Top-Kernanforderungen für die Entwicklung

### 1. Präzise Grid-Steuerung & Input-Buffering
* **Grid-System:** Bewegung in festen Zeitintervallen (Tick-Rate, z. B. 100 ms) auf einem 2D-Raster.
* **Input-Buffer:** Speicherung der nächsten gültigen Richtungsentscheidung in einer Queue. Dies verhindert versehentliche 180°-Kehrtwenden innerhalb desselben Ticks („Selbstmord-Spurn“), wenn Tasten schnell hintereinander gedrückt werden.

### 2. Zuverlässige Kollision & Futter-Spawning
* **Kollisionserkennung:** Bei jedem Tick wird geprüft: Kopf trifft Wand, Kopf trifft Schlangenkörper, Kopf trifft Futter.
* **Spawning-Garantie:** Bei Futteraufnahme wächst die Schlange um ein Segment. Neues Futter darf **niemals** auf Feldern gespawnt werden, die aktuell vom Schlangenkörper besetzt sind.

### 3. Game State Management & Progression
* **Zustandssteuerung:** Sauberes Menü für *Start*, *Pause* (z. B. `Space`/`ESC`) und *Game Over*.
* **Highscore & Dynamik:** Lokale Highscore-Speicherung (`localStorage`) und schrittweise Geschwindigkeitssteigerung mit höherem Punktestand für anhaltende Motivation.
