"""Модуль парсинга командной строки."""

import shlex


def parse_command(line: str) -> tuple[str, list[str]]:
    """Разбирает строку на команду и список аргументов.

    :param line: Входная строка.
    :return: Кортеж (команда, список аргументов).
    """
    try:
        parts = shlex.split(line.strip())
        if not parts:
            return "", []
        return parts[0], parts[1:]
    except ValueError:
        return "", []