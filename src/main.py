import tkinter as tk
from tkinter import scrolledtext
import getpass
import socket
import shlex
import argparse
import json
from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self, log_path: str | None) -> None:
        self.log_path = Path(log_path) if log_path else None

    def log_event(self, command: str, error: str | None = None) -> None:
        if not self.log_path:
            return
        event = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "error": error
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

class TerminalEmulator:
    def __init__(self, root: tk.Tk, config: dict) -> None:
        self.root = root
        self.config = config
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.logger = Logger(config.get("log_file"))
        
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
        
        self.print_to_console("--- Параметры запуска ---")
        self.print_to_console(f"VFS: {self.config.get('vfs_path')}")
        self.print_to_console(f"Log: {self.config.get('log_file')}")
        self.print_to_console(f"Script: {self.config.get('startup_script')}")
        self.print_to_console("-------------------------")

        if self.config.get("startup_script"):
            self.run_startup_script(self.config["startup_script"])

    def print_to_console(self, text: str) -> None:
        self.output_area.config(state='normal')
        self.output_area.insert(tk.END, text + "\n")
        self.output_area.see(tk.END)
        self.output_area.config(state='disabled')

    def run_startup_script(self, script_path: str) -> None:
        path = Path(script_path)
        if not path.exists():
            self.print_to_console(f"Ошибка: Скрипт не найден {script_path}")
            return
            
        self.print_to_console(f"Запуск скрипта: {script_path}")
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                cmd = line.strip()
                if not cmd or cmd.startswith("#"):
                    continue
                self.print_to_console(f"[{self.username}@{self.hostname}]$ {cmd}")
                success = self.execute_command(cmd, is_script=True)
                if not success:
                    self.print_to_console("Скрипт остановлен из-за ошибки.")
                    break

    def process_command(self, event) -> None:
        raw_command = self.input_area.get().strip()
        self.input_area.delete(0, tk.END)
        if not raw_command:
            return
        self.print_to_console(f"[{self.username}@{self.hostname}]$ {raw_command}")
        self.execute_command(raw_command, is_script=False)

    def execute_command(self, raw_command: str, is_script: bool) -> bool:
        try:
            args = shlex.split(raw_command)
        except ValueError as e:
            self.handle_error(raw_command, f"Ошибка парсинга: {e}")
            return False

        if not args:
            return True

        command = args[0]
        command_args = args[1:]

        if command == "exit":
            if not is_script:
                self.root.quit()
            return True
        elif command in ["ls", "cd"]:
            args_str = " ".join(command_args)
            self.print_to_console(f"Заглушка: {command} {args_str}".strip())
            return True
        else:
            self.handle_error(raw_command, f"Команда не найдена: {command}")
            return False

    def handle_error(self, raw_command: str, error_msg: str) -> None:
        self.print_to_console(f"Ошибка: {error_msg}")
        self.logger.log_event(raw_command, error_msg)

def parse_args() -> dict:
    parser = argparse.ArgumentParser(description="Эмулятор оболочки ОС")
    parser.add_argument("--vfs", type=str, help="Путь к VFS", default=None)
    parser.add_argument("--log", type=str, help="Путь к лог-файлу", default=None)
    parser.add_argument("--script", type=str, help="Путь к стартовому скрипту", default=None)
    
    args = parser.parse_args()
    return {
        "vfs_path": args.vfs,
        "log_file": args.log,
        "startup_script": args.script
    }

def main() -> None:
    config = parse_args()
    root = tk.Tk()
    app = TerminalEmulator(root, config)
    root.mainloop()

if __name__ == "__main__":
    main()