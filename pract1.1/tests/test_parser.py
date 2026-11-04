"""Тесты для модуля парсера."""

import unittest

from src.parser import parse_command


class TestParser(unittest.TestCase):
    """Тестирование функции parse_command."""

    def test_simple_command(self) -> None:
        """Тест простой команды без аргументов."""
        self.assertEqual(parse_command("ls"), ("ls", []))

    def test_command_with_args(self) -> None:
        """Тест команды с аргументами."""
        self.assertEqual(parse_command("ls -la"), ("ls", ["-la"]))

    def test_command_with_quotes(self) -> None:
        """Тест команды с аргументами в кавычках."""
        self.assertEqual(
            parse_command('cd "Моя папка"'), ("cd", ["Моя папка"])
        )

    def test_empty_string(self) -> None:
        """Тест пустой строки."""
        self.assertEqual(parse_command(""), ("", []))

    def test_unclosed_quote(self) -> None:
        """Тест незакрытой кавычки."""
        self.assertEqual(parse_command('ls "abc'), ("", []))


if __name__ == "__main__":
    unittest.main()