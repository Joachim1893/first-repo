import tkinter as tk
from tkinter import ttk
import random
import os

GRID_SIZE = 20
CELL_SIZE = 20
CANVAS_SIZE = GRID_SIZE * CELL_SIZE  # 400px

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Klassisches Snake Spiel")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        self.high_score_file = os.path.join(os.path.dirname(__file__), "highscore.txt")
        self.high_score = self.load_high_score()

        self.snake = []
        self.direction = (1, 0) # Right
        self.input_buffer = []
        self.food = (0, 0)
        self.score = 0
        self.game_state = "IDLE"  # "IDLE", "RUNNING", "PAUSED", "GAME_OVER"
        self.speed = 120  # ms tick rate
        self.timer_id = None

        self.setup_ui()
        self.init_game()
        self.bind_controls()

    def load_high_score(self):
        if os.path.exists(self.high_score_file):
            try:
                with open(self.high_score_file, "r") as f:
                    return int(f.read().strip())
            except ValueError:
                return 0
        return 0

    def save_high_score(self):
        try:
            with open(self.high_score_file, "w") as f:
                f.write(str(self.high_score))
        except Exception as e:
            print("Fehler beim Speichern des Highscores:", e)

    def setup_ui(self):
        # Style configuration
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TFrame", background="#1E1E1E")
        style.configure("TLabel", background="#1E1E1E", foreground="#E0E0E0", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("TMenubutton", font=("Segoe UI", 10))

        # Main Container
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(expand=True, fill="both")

        # Title
        title_label = tk.Label(
            main_frame, text="SNAKE", font=("Segoe UI", 20, "bold"),
            bg="#1E1E1E", fg="#00FF66"
        )
        title_label.pack(pady=(0, 10))

        # Scoreboard
        score_frame = tk.Frame(main_frame, bg="#2A2A2A", padx=15, pady=8)
        score_frame.pack(fill="x", pady=(0, 10))

        self.score_label = tk.Label(
            score_frame, text=f"Score: 0", font=("Segoe UI", 11, "bold"),
            bg="#2A2A2A", fg="#00FF66"
        )
        self.score_label.pack(side="left")

        self.high_score_label = tk.Label(
            score_frame, text=f"Highscore: {self.high_score}", font=("Segoe UI", 11, "bold"),
            bg="#2A2A2A", fg="#00FF66"
        )
        self.high_score_label.pack(side="right")

        # Canvas Wrapper & Canvas
        canvas_wrapper = tk.Frame(main_frame, bg="#333333", bd=2, relief="solid")
        canvas_wrapper.pack()

        self.canvas = tk.Canvas(
            canvas_wrapper, width=CANVAS_SIZE, height=CANVAS_SIZE,
            bg="#1A1A1A", highlightthickness=0
        )
        self.canvas.pack()

        # Controls & Settings Frame
        controls_frame = tk.Frame(main_frame, bg="#1E1E1E")
        controls_frame.pack(fill="x", pady=(15, 0))

        # Wall Mode Selector
        mode_frame = tk.Frame(controls_frame, bg="#252525", padx=10, pady=6)
        mode_frame.pack(fill="x", pady=(0, 10))

        mode_lbl = tk.Label(mode_frame, text="Wand-Mechanik:", bg="#252525", fg="#E0E0E0", font=("Segoe UI", 10))
        mode_lbl.pack(side="left")

        self.wall_mode_var = tk.StringVar(value="die")
        self.wall_mode_combo = ttk.Combobox(
            mode_frame, textvariable=self.wall_mode_var, state="readonly", width=24
        )
        self.wall_mode_combo['values'] = ("Tödliche Wände (Klassisch)", "Durchgleiten (Wrap-Around)")
        self.wall_mode_combo.current(0)
        self.wall_mode_combo.pack(side="right")

        # Buttons
        btn_frame = tk.Frame(controls_frame, bg="#1E1E1E")
        btn_frame.pack(fill="x")

        self.start_btn = tk.Button(
            btn_frame, text="Spiel starten", font=("Segoe UI", 10, "bold"),
            bg="#00FF66", fg="#121212", activebackground="#00CC52",
            bd=0, padx=10, pady=8, cursor="hand2", command=self.start_game
        )
        self.start_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.pause_btn = tk.Button(
            btn_frame, text="Pause", font=("Segoe UI", 10, "bold"),
            bg="#444444", fg="#FFFFFF", activebackground="#555555",
            bd=0, padx=10, pady=8, cursor="hand2", state="disabled", command=self.toggle_pause
        )
        self.pause_btn.pack(side="right", expand=True, fill="x", padx=(5, 0))

        # Instructions
        inst_label = tk.Label(
            main_frame, text="Steuerung: Pfeiltasten / WASD | Pause: Leertaste",
            font=("Segoe UI", 8), bg="#1E1E1E", fg="#888888"
        )
        inst_label.pack(pady=(12, 0))

    def init_game(self):
        self.snake = [
            (5, 10),
            (4, 10),
            (3, 10)
        ]
        self.direction = (1, 0)
        self.input_buffer = []
        self.score = 0
        self.speed = 120
        self.score_label.config(text=f"Score: {self.score}")
        self.spawn_food()
        self.draw()

    def spawn_food(self):
        empty_cells = [
            (x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)
            if (x, y) not in self.snake
        ]
        if empty_cells:
            self.food = random.choice(empty_cells)

    def bind_controls(self):
        self.root.bind("<Up>", lambda e: self.queue_input((0, -1)))
        self.root.bind("<Down>", lambda e: self.queue_input((0, 1)))
        self.root.bind("<Left>", lambda e: self.queue_input((-1, 0)))
        self.root.bind("<Right>", lambda e: self.queue_input((1, 0)))

        self.root.bind("<w>", lambda e: self.queue_input((0, -1)))
        self.root.bind("<W>", lambda e: self.queue_input((0, -1)))
        self.root.bind("<s>", lambda e: self.queue_input((0, 1)))
        self.root.bind("<S>", lambda e: self.queue_input((0, 1)))
        self.root.bind("<a>", lambda e: self.queue_input((-1, 0)))
        self.root.bind("<A>", lambda e: self.queue_input((-1, 0)))
        self.root.bind("<d>", lambda e: self.queue_input((1, 0)))
        self.root.bind("<D>", lambda e: self.queue_input((1, 0)))

        self.root.bind("<space>", lambda e: self.toggle_pause())

    def queue_input(self, new_dir):
        if self.game_state != "RUNNING":
            return
        last_dir = self.input_buffer[-1] if self.input_buffer else self.direction
        # Block instant 180 degree reversal
        if new_dir[0] + last_dir[0] == 0 and new_dir[1] + last_dir[1] == 0:
            return
        if len(self.input_buffer) < 2:
            self.input_buffer.append(new_dir)

    def start_game(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.init_game()
        self.game_state = "RUNNING"
        self.start_btn.config(text="Neu starten")
        self.pause_btn.config(state="normal", text="Pause")
        self.game_loop()

    def toggle_pause(self):
        if self.game_state == "RUNNING":
            self.game_state = "PAUSED"
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            self.pause_btn.config(text="Weiter")
            self.draw_overlay("PAUSE", "#00FF66", "Drücke [Weiter] oder [Leertaste]")
        elif self.game_state == "PAUSED":
            self.game_state = "RUNNING"
            self.pause_btn.config(text="Pause")
            self.game_loop()

    def trigger_game_over(self, reason):
        self.game_state = "GAME_OVER"
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.pause_btn.config(state="disabled")
        self.draw_overlay("GAME OVER", "#FF4444", f"{reason}\nEndstand: {self.score} Punkte")

    def game_loop(self):
        if self.game_state != "RUNNING":
            return

        if self.input_buffer:
            self.direction = self.input_buffer.pop(0)

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        is_wrap = "Wrap-Around" in self.wall_mode_combo.get()

        # Wall Collision Check
        if not is_wrap:
            if new_head[0] < 0 or new_head[0] >= GRID_SIZE or new_head[1] < 0 or new_head[1] >= GRID_SIZE:
                self.trigger_game_over("Du bist gegen die Wand gefahren!")
                return
        else:
            new_head = (new_head[0] % GRID_SIZE, new_head[1] % GRID_SIZE)

        # Self Collision Check
        if new_head in self.snake:
            self.trigger_game_over("Du hast dich selbst gebissen!")
            return

        # Move Snake
        self.snake.insert(0, new_head)

        # Check Food Collision
        if new_head == self.food:
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")
            if self.score > self.high_score:
                self.high_score = self.score
                self.high_score_label.config(text=f"Highscore: {self.high_score}")
                self.save_high_score()
            self.spawn_food()
            self.speed = max(50, 120 - (self.score // 50) * 10)
        else:
            self.snake.pop()

        self.draw()
        self.timer_id = self.root.after(self.speed, self.game_loop)

    def draw(self):
        self.canvas.delete("all")

        # Draw Grid Lines
        for i in range(GRID_SIZE):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, CANVAS_SIZE, fill="#222222")
            self.canvas.create_line(0, i * CELL_SIZE, CANVAS_SIZE, i * CELL_SIZE, fill="#222222")

        # Draw Food (Apple)
        fx, fy = self.food
        x1 = fx * CELL_SIZE + 2
        y1 = fy * CELL_SIZE + 2
        x2 = (fx + 1) * CELL_SIZE - 2
        y2 = (fy + 1) * CELL_SIZE - 2
        self.canvas.create_oval(x1, y1, x2, y2, fill="#FF4444", outline="")
        # Leaf
        self.canvas.create_oval(x1 + 6, y1 - 1, x1 + 11, y1 + 3, fill="#00FF66", outline="")

        # Draw Snake
        for idx, (sx, sy) in enumerate(self.snake):
            px1 = sx * CELL_SIZE + 1
            py1 = sy * CELL_SIZE + 1
            px2 = (sx + 1) * CELL_SIZE - 1
            py2 = (sy + 1) * CELL_SIZE - 1

            if idx == 0:
                # Head
                self.canvas.create_rectangle(px1, py1, px2, py2, fill="#00FF66", outline="")
                # Eyes
                dx, dy = self.direction
                if dx == 1: # Right
                    e1, e2 = (px2-4, py1+4, px2-2, py1+6), (px2-4, py2-6, px2-2, py2-4)
                elif dx == -1: # Left
                    e1, e2 = (px1+2, py1+4, px1+4, py1+6), (px1+2, py2-6, px1+4, py2-4)
                elif dy == -1: # Up
                    e1, e2 = (px1+4, py1+2, px1+6, py1+4), (px2-6, py1+2, px2-4, py1+4)
                else: # Down
                    e1, e2 = (px1+4, py2-4, px1+6, py2-2), (px2-6, py2-4, px2-4, py2-2)
                self.canvas.create_oval(*e1, fill="#121212", outline="")
                self.canvas.create_oval(*e2, fill="#121212", outline="")
            else:
                # Body
                self.canvas.create_rectangle(px1+1, py1+1, px2-1, py2-1, fill="#00CC52", outline="")

        if self.game_state == "IDLE":
            self.draw_overlay("SNAKE GAME", "#00FF66", "Klicke auf 'Spiel starten' um loszulegen!")

    def draw_overlay(self, title, color, text):
        self.canvas.create_rectangle(0, 0, CANVAS_SIZE, CANVAS_SIZE, fill="#000000", stipple="gray50", outline="")
        self.canvas.create_text(
            CANVAS_SIZE // 2, CANVAS_SIZE // 2 - 25,
            text=title, font=("Segoe UI", 22, "bold"), fill=color
        )
        self.canvas.create_text(
            CANVAS_SIZE // 2, CANVAS_SIZE // 2 + 20,
            text=text, font=("Segoe UI", 11), fill="#FFFFFF", justify="center"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = SnakeGame(root)
    root.mainloop()
