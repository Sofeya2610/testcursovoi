import subprocess
import os


class GameBackend:
    def __init__(self, exe_path: str):
        self.exe_path = exe_path
        self.proc: subprocess.Popen | None = None

    def start(self) -> bool:
        """Запустити C++ гру і відправити команду START."""
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

            self.proc.stdin.write("START\n")
            self.proc.stdin.flush()

            response = self.proc.stdout.readline().strip()
            # print("BACKEND START:", repr(response))
            return "READY" in response
        except Exception:
            self.proc = None
            return False

    def send_guess(self, word: str) -> str:
        """Надіслати слово, отримати відповідь (FEEDBACK/ WIN/ INVALID)."""
        if not self.proc:
            return "ERROR: NO PROCESS"

        try:
            self.proc.stdin.write(word + "\n")
            self.proc.stdin.flush()
            response = self.proc.stdout.readline().strip()
            # print("BACKEND GUESS:", repr(response))
            return response
        except Exception as e:
            return f"ERROR: {e}"

    def request_hint(self) -> str:
        """Запросити підказку, отримати відповідь HINT ..."""
        if not self.proc:
            return "ERROR: NO PROCESS"

        try:
            self.proc.stdin.write("HINT\n")
            self.proc.stdin.flush()
            response = self.proc.stdout.readline().strip()
            # print("BACKEND HINT:", repr(response))
            return response
        except Exception as e:
            return f"ERROR: {e}"

    def stop(self):
        if self.proc:
            try:
                self.proc.terminate()
            except Exception:
                pass
            self.proc = None
