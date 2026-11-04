"""Модуль логирования событий."""

import datetime
import json
import os


def log_event(log_path: str, command: str, error: str = "") -> None:
    """Записывает событие в JSON-файл.

    :param log_path: Путь к файлу лога.
    :param command: Введенная команда.
    :param error: Текст ошибки (если есть).
    """
    event = {
        "date": datetime.datetime.now().isoformat(),
        "command": command,
        "error": error,
    }

    logs = []
    if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
                if not isinstance(logs, list):
                    logs = []
            except json.JSONDecodeError:
                logs = []

    logs.append(event)

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=4)