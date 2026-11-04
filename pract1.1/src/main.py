"""Эмулятор оболочки ОС."""

import argparse
import getpass
import platform
import socket
import tkinter as tk
from tkinter import scrolledtext

from src.logger import log_event
from src.parser import parse_command
from src.vfs import VFS


class ShellEmulator:
    """Класс эмулятора оболочки."""

    def __init__(
        self, root: tk.Tk, vfs_path: str, log_path: str, script_path: str
    ) -> None:
        """Инициализация эмулятора."""
        self.root = root
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.os_name = platform.system()
        self.log_path = log_path
        self.script_path = script_path
        self.vfs = VFS(vfs_path)

        self.root.title(f"Эмулятор - [{self.username}@{self.hostname}]")
        self.root.geometry("600x400")
        self._setup_ui()

        print(f"VFS Path: {vfs_path}")
        print(f"Log Path: {log_path}")
        print(f"Script Path: {script_path}")

    def _setup_ui(self) -> None:
        """Настройка графического интерфейса."""
        self.entry = tk.Entry(self.root)
        self.entry.pack(side="bottom", fill="x", padx=5, pady=5)
        self.entry.bind("<Return>", self._process_input)

        self.text_area = scrolledtext.ScrolledText(
            self.root, state="disabled", wrap="word"
        )
        self.text_area.pack(
            side="top", fill="both", expand=True, padx=5, pady=5
        )

        self._append_text(f"Добро пожаловать в эмулятор {self.os_name}!\n")

        if self.script_path:
            self.root.after(100, self._run_script)

    def _append_text(self, text: str) -> None:
        """Добавляет текст в текстовое поле."""
        self.text_area.config(state="normal")
        self.text_area.insert("end", text)
        self.text_area.see("end")
        self.text_area.config(state="disabled")

    def _run_script(self) -> None:
        """Выполняет стартовый скрипт."""
        try:
            with open(self.script_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        self._append_text(
                            f"{self.username}@{self.hostname}"
                            f":{self.vfs.current_path}$ {line}\n"
                        )
                        success = self._execute_command(line, is_script=True)
                        if not success:
                            self._append_text(
                                "Выполнение скрипта остановлено.\n"
                            )
                            break
        except FileNotFoundError:
            self._append_text(
                f"Ошибка: скрипт {self.script_path} не найден.\n"
            )

    def _process_input(self, event: tk.Event) -> None:
        """Обрабатывает ввод пользователя."""
        line = self.entry.get()
        self.entry.delete(0, "end")
        self._append_text(
            f"{self.username}@{self.hostname}:{self.vfs.current_path}$ {line}\n"
        )
        self._execute_command(line)

    def _execute_command(self, line: str, is_script: bool = False) -> bool:
        """Выполняет команду и логирует результат."""
        cmd, args = parse_command(line)
        if not cmd:
            return True

        error_msg = ""
        if cmd == "exit":
            log_event(self.log_path, line)
            self.root.quit()
            return True
        elif cmd == "ls":
            result = self.vfs.ls(args)
            if result.startswith("ls:"):
                error_msg = result
                self._append_text(f"{result}\n")
                log_event(self.log_path, line, error_msg)
                return False
            if result:
                self._append_text(f"{result}\n")
        elif cmd == "cd":
            result = self.vfs.cd(args)
            if result:
                error_msg = result
                self._append_text(f"{result}\n")
                log_event(self.log_path, line, error_msg)
                return False
        else:
            error_msg = f"команда '{cmd}' не найдена"
            self._append_text(f"Ошибка: {error_msg}.\n")
            log_event(self.log_path, line, error_msg)
            return False

        log_event(self.log_path, line, error_msg)
        return True


def main() -> None:
    """Точка входа в приложение."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки ОС")
    parser.add_argument(
        "--vfs", type=str, default="./vfs", help="Путь к VFS"
    )
    parser.add_argument(
        "--log",
        type=str,
        default="./logs/log.json",
        help="Путь к лог-файлу",
    )
    parser.add_argument(
        "--script", type=str, default="", help="Путь к стартовому скрипту"
    )

    args = parser.parse_args()

    root = tk.Tk()
    app = ShellEmulator(root, args.vfs, args.log, args.script)
    root.mainloop()


if __name__ == "__main__":
    main()