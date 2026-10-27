import tkinter as tk
from tkinter import scrolledtext
import getpass
import socket
import shlex


class TerminalEmulator:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()

        self.root.title(f"Эмулятор - [{self.username}@{self.hostname}]")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        self.output_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state='disabled',
            bg="black", fg="white", font=("Consolas", 12)
        )
        self.output_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_area = tk.Entry(
            self.root, bg="black", fg="white",
            insertbackground="white", font=("Consolas", 12)
        )
        self.input_area.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.input_area.bind("<Return>", self.process_command)
        self.input_area.focus()

        self.print_to_console(f"Добро пожаловать в эмулятор, {self.username}!")

    def print_to_console(self, text: str) -> None:
        self.output_area.config(state='normal')
        self.output_area.insert(tk.END, text + "\n")
        self.output_area.see(tk.END)
        self.output_area.config(state='disabled')

    def process_command(self, event) -> None:
        raw_command = self.input_area.get().strip()
        self.input_area.delete(0, tk.END)

        self.print_to_console(f"[{self.username}@{self.hostname}]$ {raw_command}")

        if not raw_command:
            return

        try:
            args = shlex.split(raw_command)
        except ValueError as e:
            self.print_to_console(f"Ошибка парсинга: {e}")
            return

        command = args[0]
        command_args = args[1:]

        if command == "exit":
            self.root.quit()
        elif command in ["ls", "cd"]:
            args_str = " ".join(command_args)
            self.print_to_console(f"Заглушка: команда {command}, аргументы: {args_str}")
        else:
            self.print_to_console(f"Команда не найдена: {command}")


def main() -> None:
    root = tk.Tk()
    app = TerminalEmulator(root)
    root.mainloop()


if __name__ == "__main__":
    main() 
