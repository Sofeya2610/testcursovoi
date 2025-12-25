import subprocess
import os


class GameBackend:
    def __init__(self, exe_path: str):
        self.exe_path = exe_path
        self.proc: subprocess.Popen | None = None

    def start_process(self) -> bool:
        """Запустити C++ процес без команд."""
        if self.proc:
            try:
                self.proc.terminate()
            except Exception:
                pass

        creation_flags = 0
        if os.name == "nt":
            creation_flags = subprocess.CREATE_NO_WINDOW

        try:
            self.proc = subprocess.Popen(
                [self.exe_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                bufsize=1,
                creationflags=creation_flags
            )
            return True
        except Exception:
            self.proc = None
            return False

    def send_line(self, line: str) -> str:
        """Надіслати рядок у C++ і прочитати відповідь."""
        if not self.proc:
            return "ERROR: NO PROCESS"
        try:
            self.proc.stdin.write(line + "\n")
            self.proc.stdin.flush()
            resp = self.proc.stdout.readline().strip()
            return resp
        except Exception as e:
            return f"ERROR: {e}"

    def set_mode(self, mode: str) -> str:
        """MODE EASY / MODE HARD"""
        return self.send_line(f"MODE {mode}")

    def start_game(self) -> str:
        """Команда START (після вибору режиму)."""
        return self.send_line("START")

    def send_guess(self, word: str) -> str:
        return self.send_line(word)

    def request_hint(self) -> str:
        return self.send_line("HINT")

    def stop(self):
        if self.proc:
            try:
                self.proc.terminate()
            except Exception:
                pass
            self.proc = None
