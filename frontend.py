import tkinter as tk
from tkinter import messagebox

from backend_client import GameBackend

WORD_LENGTH = 5
MAX_ATTEMPTS = 5
EXE_PATH = "./game_logic.exe"

BG_COLOR = "#121213"
CELL_BG = "#3a3a3c"
GREEN = "#538d4e"
YELLOW = "#b59f3b"
GRAY = "#3a3a3c"


class WordleApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Guess the Word (C++ + Python)")
        self.root.geometry("520x760")
        self.root.configure(bg=BG_COLOR)

        # бекенд C++
        self.backend = GameBackend(EXE_PATH)

        # стан гри
        self.current_attempt = 0
        self.game_running = False
        self.hint_used = False
        self.difficulty = "EASY"  # EASY або HARD

        # статистика
        self.games_played = 0
        self.games_won = 0
        self.score = 0

        # два екрани
        self.menu_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.game_frame = tk.Frame(self.root, bg=BG_COLOR)

        self.create_menu_ui()
        self.create_game_ui()

        self.show_menu()

    # ------------------ MENU UI ------------------

    def create_menu_ui(self):
        title = tk.Label(
            self.menu_frame,
            text="WORD GUESS GAME",
            font=("Arial", 28, "bold"),
            bg=BG_COLOR,
            fg="white",
            pady=40
        )
        title.pack()

        # Вибір складності
        diff_label = tk.Label(
            self.menu_frame,
            text="Choose difficulty:",
            font=("Arial", 14),
            bg=BG_COLOR,
            fg="white",
            pady=10
        )
        diff_label.pack()

        self.menu_mode_var = tk.StringVar(value="EASY")

        diff_frame = tk.Frame(self.menu_frame, bg=BG_COLOR)
        diff_frame.pack(pady=5)

        tk.Radiobutton(
            diff_frame, text="Easy", variable=self.menu_mode_var, value="EASY",
            font=("Arial", 12),
            bg=BG_COLOR, fg="white", selectcolor=BG_COLOR,
            activebackground=BG_COLOR, activeforeground="white"
        ).pack(side=tk.LEFT, padx=10)

        tk.Radiobutton(
            diff_frame, text="Hard", variable=self.menu_mode_var, value="HARD",
            font=("Arial", 12),
            bg=BG_COLOR, fg="white", selectcolor=BG_COLOR,
            activebackground=BG_COLOR, activeforeground="white"
        ).pack(side=tk.LEFT, padx=10)

        # Кнопки меню
        btn_frame = tk.Frame(self.menu_frame, bg=BG_COLOR)
        btn_frame.pack(pady=40)

        start_btn = tk.Button(
            btn_frame,
            text="START GAME",
            command=self.start_from_menu,
            font=("Arial", 14, "bold"),
            bg="#565758",
            fg="white",
            width=15,
            height=2,
            activebackground="#818384"
        )
        start_btn.grid(row=0, column=0, padx=5, pady=5)

        stats_btn = tk.Button(
            btn_frame,
            text="SHOW STATS",
            command=self.show_stats,
            font=("Arial", 14, "bold"),
            bg="#565758",
            fg="white",
            width=15,
            height=2
        )
        stats_btn.grid(row=1, column=0, padx=5, pady=5)

        exit_btn = tk.Button(
            btn_frame,
            text="EXIT",
            command=self.root.destroy,
            font=("Arial", 14, "bold"),
            bg="#565758",
            fg="white",
            width=15,
            height=2
        )
        exit_btn.grid(row=2, column=0, padx=5, pady=5)

    def start_from_menu(self):
        self.difficulty = self.menu_mode_var.get()
        self.show_game()
        self.start_new_game()

    def show_menu(self):
        self.game_frame.pack_forget()
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

    def show_game(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack(fill=tk.BOTH, expand=True)

    def show_stats(self):
        if self.games_played == 0:
            win_rate = 0.0
        else:
            win_rate = (self.games_won / self.games_played) * 100.0

        msg = (
            f"Games played: {self.games_played}\n"
            f"Games won: {self.games_won}\n"
            f"Win rate: {win_rate:.1f}%\n"
            f"Score: {self.score}"
        )
        messagebox.showinfo("Statistics", msg)

    # ------------------ GAME UI ------------------

    def create_game_ui(self):
        title_label = tk.Label(
            self.game_frame,
            text="GUESS THE WORD",
            font=("Arial", 26, "bold"),
            bg=BG_COLOR,
            fg="white",
            pady=20
        )
        title_label.pack()

        # Кнопка повернення до меню
        top_btn_frame = tk.Frame(self.game_frame, bg=BG_COLOR)
        top_btn_frame.pack(pady=5)

        back_btn = tk.Button(
            top_btn_frame,
            text="MENU",
            command=self.back_to_menu,
            font=("Arial", 10, "bold"),
            bg="#565758",
            fg="white",
            width=8,
            height=1
        )
        back_btn.pack()

        self.grid_frame = tk.Frame(self.game_frame, bg=BG_COLOR)
        self.grid_frame.pack(pady=10)

        self.cells = []
        for r in range(MAX_ATTEMPTS):
            row_cells = []
            for c in range(WORD_LENGTH):
                cell = tk.Label(
                    self.grid_frame,
                    text="",
                    font=("Arial", 24, "bold"),
                    width=3,
                    height=1,
                    fg="white",
                    bg=CELL_BG,
                    highlightthickness=2,
                    highlightbackground="#565758"
                )
                cell.grid(row=r, column=c, padx=5, pady=5)
                row_cells.append(cell)
            self.cells.append(row_cells)

        self.entry = tk.Entry(
            self.game_frame,
            font=("Arial", 20),
            width=10,
            justify="center",
            insertbackground="white",
            bg="#272728",
            fg="white",
            border=0
        )
        self.entry.pack(pady=20)
        self.entry.bind("<Return>", lambda event: self.submit_guess())
        self.entry.focus_set()

        btn_frame = tk.Frame(self.game_frame, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        self.submit_btn = tk.Button(
            btn_frame,
            text="GUESS",
            command=self.submit_guess,
            font=("Arial", 12, "bold"),
            bg="#565758",
            fg="white",
            width=10,
            height=2,
            activebackground="#818384"
        )
        self.submit_btn.grid(row=0, column=0, padx=5)

        hint_btn = tk.Button(
            btn_frame,
            text="HINT",
            command=self.request_hint,
            font=("Arial", 12, "bold"),
            bg="#565758",
            fg="white",
            width=10,
            height=2
        )
        hint_btn.grid(row=0, column=1, padx=5)

        new_game_btn = tk.Button(
            btn_frame,
            text="NEW GAME",
            command=self.start_new_game,
            font=("Arial", 12, "bold"),
            bg="#565758",
            fg="white",
            width=10,
            height=2
        )
        new_game_btn.grid(row=0, column=2, padx=5)

        self.status_label = tk.Label(
            self.game_frame,
            text="",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg="white"
        )
        self.status_label.pack(pady=10)

        self.score_label = tk.Label(
            self.game_frame,
            text="Score: 0",
            font=("Arial", 12, "bold"),
            bg=BG_COLOR,
            fg="white"
        )
        self.score_label.pack(pady=5)

    def back_to_menu(self):
        # при поверненні просто зупиняємо бекенд
        self.backend.stop()
        self.show_menu()

    # ------------------ GAME LOGIC ------------------

    def start_new_game(self):
        self.backend.stop()

        self.current_attempt = 0
        self.game_running = False
        self.hint_used = False
        self.entry.delete(0, tk.END)
        self.submit_btn.config(state=tk.NORMAL)

        for r in range(MAX_ATTEMPTS):
            for c in range(WORD_LENGTH):
                self.cells[r][c].config(text="", bg=CELL_BG)

        ok = self.backend.start_process()
        if not ok:
            self.status_label.config(
                text="Error starting C++ process.",
                fg="red"
            )
            return

        # встановлюємо режим
        resp_mode = self.backend.set_mode(self.difficulty)
        # print("MODE RESP:", repr(resp_mode))

        # START
        resp_start = self.backend.start_game()
        # print("START RESP:", repr(resp_start))

        if "READY" in resp_start:
            self.game_running = True
            self.status_label.config(
                text=f"Game started ({self.difficulty}). Enter a 5-letter word.",
                fg="white"
            )
        else:
            self.status_label.config(
                text="Error starting game (no READY).",
                fg="red"
            )

    def submit_guess(self):
        if not self.game_running:
            return

        guess = self.entry.get().strip()
        if len(guess) != WORD_LENGTH:
            messagebox.showwarning(
                "Warning",
                f"Word must have {WORD_LENGTH} letters."
            )
            return

        response = self.backend.send_guess(guess)
        # print("RESP GUESS:", repr(response))

        if "FEEDBACK" in response or "WIN" in response:
            parts = response.split()
            feedback = parts[-1]

            self.show_feedback(guess.upper(), feedback)

            if "WIN" in response:
                self.game_running = False
                self.submit_btn.config(state=tk.DISABLED)

                # оновити статистику
                self.games_played += 1
                self.games_won += 1

                # простий підрахунок очок
                base_score = 10
                penalty = self.current_attempt
                hint_penalty = 2 if self.hint_used else 0
                gain = max(1, base_score - penalty - hint_penalty)
                self.score += gain
                self.score_label.config(text=f"Score: {self.score}")

                self.status_label.config(
                    text="YOU WIN!",
                    fg=GREEN
                )
                messagebox.showinfo(
                    "Win",
                    f"You guessed the word: {guess.upper()}\n"
                    f"+{gain} score"
                )
            else:
                self.current_attempt += 1
                self.entry.delete(0, tk.END)

                if self.current_attempt >= MAX_ATTEMPTS:
                    self.game_running = False
                    self.submit_btn.config(state=tk.DISABLED)

                    self.games_played += 1  # програш, але гра зіграна

                    self.status_label.config(
                        text="GAME OVER.",
                        fg="red"
                    )
                    messagebox.showinfo(
                        "Lose",
                        "No attempts left. Try again!"
                    )
        elif "INVALID" in response:
            self.status_label.config(
                text="Invalid input.",
                fg="orange"
            )

    def request_hint(self):
        if not self.game_running:
            return
        if self.hint_used:
            messagebox.showinfo("Hint", "You have already used the hint.")
            return

        response = self.backend.request_hint()
        # print("RESP HINT:", repr(response))

        if response.startswith("HINT"):
            parts = response.split()
            if len(parts) == 3:
                pos_str, letter = parts[1], parts[2]
                try:
                    pos = int(pos_str)
                except ValueError:
                    messagebox.showinfo("Hint", "No hint available.")
                    return

                self.hint_used = True
                messagebox.showinfo(
                    "Hint",
                    f"Letter at position {pos + 1} is: {letter}"
                )
            else:
                messagebox.showinfo("Hint", "No hint available.")

    def show_feedback(self, guess: str, feedback: str):
        row = self.current_attempt
        for i in range(WORD_LENGTH):
            char = guess[i] if i < len(guess) else ""
            code = feedback[i] if i < len(feedback) else "B"

            color = GRAY
            if code == "G":
                color = GREEN
            elif code == "Y":
                color = YELLOW

            self.cells[row][i].config(text=char, bg=color)


if __name__ == "__main__":
    root = tk.Tk()
    app = WordleApp(root)
    root.mainloop()
