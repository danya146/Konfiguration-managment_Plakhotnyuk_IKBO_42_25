def parse_test_graph(filepath):
    """
    Читает тестовый граф из файла.
    Формат строки: 'A: B C' (A зависит от B и C).
    Возвращает словарь: {'A': ['B', 'C'], ...}.
    """
    graph = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ':' in line:
                    pkg, deps_str = line.split(':', 1)
                    pkg = pkg.strip().upper()
                    deps = [d.strip().upper() for d in deps_str.split()]
                    graph[pkg] = deps
        return graph
    except FileNotFoundError:
        print(f"Ошибка: Тестовый граф не найден: {filepath}")
        return {}

def dfs_build(package, graph, depth, filter_str, visited, current_path):
    """
    Рекурсивная функция DFS для построения графа.
    Возвращает вложенный словарь зависимостей.
    """
    if depth <= 0:
        return {}
    
    if filter_str and filter_str.upper() in package.upper():
        return None
        
    # Пункт 4: Обработка цикла
    if package in current_path:
        return {"[CYCLE]": {}}
        
    if package in visited:
        return {}
    
    visited.add(package)
    current_path.add(package)
    
    children = {}
    deps = graph.get(package, [])
    
    for dep in deps:
        child_tree = dfs_build(
            dep, graph, depth - 1, filter_str, visited, current_path
        )
        if child_tree is not None:
            children[dep] = child_tree
            
    current_path.remove(package)
    return children

def build_tree(package, graph, max_depth, filter_str):
    """
    Обертка для запуска DFS.
    """
    visited = set()
    current_path = set()
    
    if filter_str and filter_str.upper() in package.upper():
        print(f"Пакет {package} исключен фильтром.")
        return {}
        
    return {package: dfs_build(
        package, graph, max_depth, filter_str, visited, current_path
    )}
def get_load_order(package, graph):
    """
    Вычисляет порядок загрузки зависимостей (топологическая сортировка).
    Возвращает список пакетов в порядке загрузки или None, если найден цикл.
    """
    visited = set()
    current_path = set()
    load_order = []

    def visit(node):
        if node in current_path:
            # Найден цикл! Топологическая сортировка невозможна.
            raise ValueError(f"Обнаружен цикл в зависимостях: {node}")
        if node in visited:
            return

        current_path.add(node)
        
        # Сначала обходим всех детей (зависимости)
        deps = graph.get(node, [])
        for dep in deps:
            visit(dep)
            
        current_path.remove(node)
        visited.add(node)
        # Добавляем узел в список ПОСЛЕ его зависимостей
        load_order.append(node)

    try:
        visit(package)
        return load_order
    except ValueError as error:
        print(f"Ошибка при построении порядка загрузки: {error}")
        return None