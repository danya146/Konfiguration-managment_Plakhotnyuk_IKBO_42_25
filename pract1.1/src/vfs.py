"""Модуль виртуальной файловой системы."""

import os


class VFS:
    """Класс для работы с виртуальной файловой системой."""

    def __init__(self, root_path: str) -> None:
        """Инициализация VFS."""
        self.root_path = os.path.abspath(root_path)
        self.current_path = "/"

    def _get_real_path(self, virtual_path: str) -> str:
        """Преобразует виртуальный путь в реальный."""
        clean = virtual_path.strip("/")
        if not clean:
            return self.root_path
        parts = clean.replace("/", "\\").split("\\")
        return os.path.join(self.root_path, *parts)

    def ls(self, args: list[str]) -> str:
        """Возвращает список файлов и папок."""
        target = args[0] if args else self.current_path
        real_path = self._get_real_path(target)

        if not os.path.exists(real_path):
            return f"ls: {target}: No such file or directory"

        if os.path.isfile(real_path):
            return target

        try:
            items = os.listdir(real_path)
            return "  ".join(items) if items else ""
        except PermissionError:
            return f"ls: {target}: Permission denied"

    def cd(self, args: list[str]) -> str:
        """Меняет текущую директорию."""
        if not args:
            self.current_path = "/"
            return ""

        target = args[0]
        
        if not target.startswith("/"):
            base = self.current_path.rstrip("/")
            target = f"{base}/{target}".replace("//", "/")

        real_path = self._get_real_path(target)

        if not os.path.exists(real_path):
            return f"cd: {target}: No such file or directory"
        if not os.path.isdir(real_path):
            return f"cd: {target}: Not a directory"

        self.current_path = target
        return ""