"""Эмулятор оболочки ОС."""

import getpass
import platform
import socket
import tkinter as tk
from tkinter import scrolledtext

from src.parser import parse_command


class ShellEmulator:
    """Класс эмулятора оболочки."""

    def __init__(self, root: tk.Tk) -> None:
        """Инициализация эмулятора.

        :param root: Корневое окно Tkinter.
        """
        self.root = root
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.os_name = platform.system()
        self.root.title(f"Эмулятор - [{self.username}@{self.hostname}]")
        self.root.geometry("600x400")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Настройка графического интерфейса."""
        self.entry = tk.Entry(self.root)
        self.entry.pack(side="bottom", fill="x", padx=5, pady=5)
        self.entry.bind("<Return>", self._process_input)

        self.text_area = scrolledtext.ScrolledText(
            self.root, state="disabled", wrap="word"
        )
        self.text_area.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        self._append_text(f"Добро пожаловать в эмулятор {self.os_name}!\n")
        self._append_text("Введите 'exit' для выхода.\n\n")

    def _append_text(self, text: str) -> None:
        """Добавляет текст в текстовое поле.

        :param text: Текст для добавления.
        """
        self.text_area.config(state="normal")
        self.text_area.insert("end", text)
        self.text_area.see("end")
        self.text_area.config(state="disabled")

    def _process_input(self, event: tk.Event) -> None:
        """Обрабатывает ввод пользователя.

        :param event: Событие нажатия Enter.
        """
        line = self.entry.get()
        self.entry.delete(0, "end")
        self._append_text(f"{self.username}@{self.hostname}:~$ {line}\n")

        cmd, args = parse_command(line)
        if not cmd:
            return

        if cmd == "exit":
            self.root.quit()
        elif cmd == "ls":
            self._append_text(f"ls: аргументы: {args}\n")
        elif cmd == "cd":
            self._append_text(f"cd: аргументы: {args}\n")
        else:
            self._append_text(f"Ошибка: команда '{cmd}' не найдена.\n")


def main() -> None:
    """Точка входа в приложение."""
    root = tk.Tk()
    app = ShellEmulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()