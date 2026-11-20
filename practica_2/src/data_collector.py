import urllib.request
import urllib.error
import json

HTTP_NOT_FOUND = 404


def get_dependencies_from_pypi(package_name, version):
    """Получает прямые зависимости из PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/{version}/json"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            requires_dist = data.get('info', {}).get('requires_dist', [])
            if not requires_dist:
                return []
            
            dependencies = []
            for req in requires_dist:
                dep_name = req.split(' ')[0].split(';')[0].strip()
                dependencies.append(dep_name)
            return dependencies
    except urllib.error.HTTPError as e:
        if e.code == HTTP_NOT_FOUND:
            raise ValueError(f"Пакет {package_name}=={version} не найден.")
        raise ValueError(f"Ошибка запроса: {e}")
    except urllib.error.URLError as e:
        raise ValueError(f"Ошибка сети: {e.reason}")


def get_dependencies_from_file(filepath, package_name):
    """Читает зависимости из локального тестового файла."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get(package_name, [])
    except FileNotFoundError:
        raise ValueError(f"Тестовый файл не найден: {filepath}")
    except json.JSONDecodeError:
        raise ValueError(f"Ошибка формата JSON в файле: {filepath}")


def get_dependencies(package_name, version, repo_url, test_mode=False):
    """Универсальная функция получения зависимостей."""
    if test_mode:
        return get_dependencies_from_file(repo_url, package_name)
    else:
        return get_dependencies_from_pypi(package_name, version)