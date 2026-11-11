import urllib.request
import urllib.error
import re

TIMEOUT_SECONDS = 10
REQUIRES_DIST_PATTERN = re.compile(
    r'^Requires-Dist:\s*([a-zA-Z0-9_\-]+)',
    re.MULTILINE | re.IGNORECASE
)

def fetch_from_url(url):
    """
    Скачивает текстовые метаданные по URL.
    Возвращает текст или None в случае ошибки.
    """
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as error:
        print(f"Сетевая ошибка при обращении к {url}: {error}")
        return None

def fetch_from_file(filepath):
    """
    Читает текстовые метаданные из локального файла.
    Возвращает текст или None в случае ошибки.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути {filepath}")
        return None

def extract_dependencies(metadata_text):
    """
    Извлекает имена прямых зависимостей из текста.
    Использует регулярное выражение для поиска строк Requires-Dist.
    """
    if not metadata_text:
        return []

    dependencies = []
    matches = REQUIRES_DIST_PATTERN.findall(metadata_text)

    for match in matches:
        dep_name = match.strip().lower()
        if dep_name not in dependencies:
            dependencies.append(dep_name)

    return dependencies