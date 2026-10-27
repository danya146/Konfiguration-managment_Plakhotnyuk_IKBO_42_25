from pathlib import Path
from typing import Any

class VFS:
    def __init__(self, source_path: str | None = None) -> None:
        self.root: dict[str, Any] = {}
        self.current_path: list[str] = []
        
        if source_path:
            self._load_from_disk(Path(source_path))

    def _load_from_disk(self, path: Path) -> None:
        if not path.exists() or not path.is_dir():
            return
        
        for item in path.iterdir():
            if item.is_dir():
                sub_vfs = VFS()
                sub_vfs._load_from_disk(item)
                self.root[item.name] = sub_vfs.root
            elif item.is_file():
                try:
                    self.root[item.name] = item.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    self.root[item.name] = "<binary_data>"

    def get_current_dir(self) -> dict[str, Any]:
        current = self.root
        for part in self.current_path:
            current = current[part]
        return current

    def ls(self) -> list[str]:
        return list(self.get_current_dir().keys())

    def cd(self, target: str) -> str | None:
        if target == "..":
            if self.current_path:
                self.current_path.pop()
            return None
            
        if target == "/":
            self.current_path = []
            return None

        current = self.get_current_dir()
        if target in current and isinstance(current[target], dict):
            self.current_path.append(target)
            return None
        return f"cd: {target}: Not a directory"

    def mkdir(self, name: str) -> str | None:
        current = self.get_current_dir()
        if name in current:
            return f"mkdir: {name}: File exists"
        current[name] = {}
        return None

    def touch(self, name: str) -> str | None:
        current = self.get_current_dir()
        if name not in current:
            current[name] = ""
        return None
        
    def cat(self, name: str) -> str:
        current = self.get_current_dir()
        if name not in current:
            return f"cat: {name}: No such file"
        if isinstance(current[name], dict):
            return f"cat: {name}: Is a directory"
        return current[name]