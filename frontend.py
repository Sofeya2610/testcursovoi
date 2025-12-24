import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# --- CONSTANTS ---
WORD_LENGTH = 5
MAX_ATTEMPTS = 5
EXE_PATH = "./game_logic.exe"

BG_COLOR = "#121213"
CELL_BG = "#3a3a3c"
GREEN = "#538d4e"
YELLOW = "#b59f3b"
GRAY = "#3a3a3c"


class WordleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess the Word (C++ + Python)")
        self.root.geometry("480x700")
        self.root.configure(bg=BG_COLOR)

        self.cpp_process = None
        self.current_attempt = 0
        self.game_running = False
        self.hint_used = False

        self.create_widgets()
        self.start_new_game()

    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="GUESS THE WORD",
            font=("Arial", 26, "bold"),
            bg=BG_COLOR,
            fg="white",
            pady=20
        )
        title_label.pack()

        self.grid_frame = tk.Frame(self.root, bg=BG_COLOR)
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
            self.root,
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

        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
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
            self.root,
            text="",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg="white"
        )
        self.status_label.pack(pady=10)

    def start_new_game(self):
        if self.cpp_process:
            try:
                self.cpp_process.terminate()
            except Exception:
                pass

        self.current_attempt = 0
        self.game_running = False
        self.hint_used = False
        self.entry.delete(0, tk.END)
        self.submit_btn.config(state=tk.NORMAL)

        for r in range(MAX_ATTEMPTS):
            for c in range(WORD_LENGTH):
                self.cells[r][c].config(text="", bg=CELL_BG)

        try:
            creation_flags = 0
            if os.name == "nt":
                creation_flags = subprocess.CREATE_NO_WINDOW

            self.cpp_process = subprocess.Popen(
                [EXE_PATH],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                bufsize=1,
                creationflags=creation_flags
            )

            self.cpp_process.stdin.write("START\n")
            self.cpp_process.stdin.flush()

            response = self.cpp_process.stdout.readline().strip()
            # print("RESP START:", repr(response))

            if "READY" in response:
                self.game_running = True
                self.status_label.config(
                    text="Game started. Enter a 5-letter English word.",
                    fg="white"
                )
            else:
                self.status_label.config(
                    text="Error starting C++ game.",
                    fg="red"
                )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Cannot start {EXE_PATH}\n{e}"
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

        try:
            self.cpp_process.stdin.write(guess + "\n")
            self.cpp_process.stdin.flush()

            response = self.cpp_process.stdout.readline().strip()
            # print("RESP GUESS:", repr(response))

            if "FEEDBACK" in response or "WIN" in response:
                parts = response.split()
                feedback = parts[-1]

                self.show_feedback(guess.upper(), feedback)

                if "WIN" in response:
                    self.game_running = False
                    self.status_label.config(
                        text="YOU WIN!",
                        fg=GREEN
                    )
                    messagebox.showinfo(
                        "Win",
                        f"You guessed the word: {guess.upper()}"
                    )
                    self.submit_btn.config(state=tk.DISABLED)
                else:
                    self.current_attempt += 1
                    self.entry.delete(0, tk.END)

                    if self.current_attempt >= MAX_ATTEMPTS:
                        self.game_running = False
                        self.status_label.config(
                            text="GAME OVER.",
                            fg="red"
                        )
                        messagebox.showinfo(
                            "Lose",
                            "No attempts left. Try again!"
                        )
                        self.submit_btn.config(state=tk.DISABLED)

            elif "INVALID" in response:
                self.status_label.config(
                    text="Invalid input.",
                    fg="orange"
                )

        except Exception as e:
            self.status_label.config(
                text=f"Connection error: {e}",
                fg="red"
            )

    def request_hint(self):
        if not self.game_running:
            return
        if self.hint_used:
            messagebox.showinfo("Hint", "You have already used the hint.")
            return

        try:
            self.cpp_process.stdin.write("HINT\n")
            self.cpp_process.stdin.flush()

            response = self.cpp_process.stdout.readline().strip()
            # print("RESP HINT:", repr(response))

            if response.startswith("HINT"):
                parts = response.split()
                if len(parts) == 3:
                    pos_str, letter = parts[1], parts[2]
                    pos = int(pos_str)
                    self.hint_used = True

                    messagebox.showinfo(
                        "Hint",
                        f"Letter at position {pos + 1} is: {letter}"
                    )
                else:
                    messagebox.showinfo("Hint", "No hint available.")

        except Exception as e:
            self.status_label.config(
                text=f"Hint error: {e}",
                fg="red"
            )

    def show_feedback(self, guess, feedback):
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
