from data_collector import get_dependencies


def build_graph(package, version, repo_url, max_depth,
                filter_str, test_mode):
    """Строит граф зависимостей с помощью рекурсивного DFS."""
    visited = set()
    graph = {}

    def dfs(current_package, current_depth):
        if current_depth >= max_depth:
            return
        if current_package in visited:
            return
        
        visited.add(current_package)

        try:
            deps = get_dependencies(
                current_package, version, repo_url, test_mode
            )
        except ValueError as e:
            deps = []
            warn_msg = f"Предупреждение: нет данных для {current_package}."
            print(f"{warn_msg} {e}")

        filtered_deps = []
        for dep in deps:
            if filter_str and filter_str in dep:
                continue
            filtered_deps.append(dep)

        graph[current_package] = filtered_deps

        for dep in filtered_deps:
            dfs(dep, current_depth + 1)

    dfs(package, 0)
    return graph


def get_install_order(graph):
    """Возвращает порядок установки пакетов."""
    visited = set()
    order = []

    def post_order_dfs(node):
        if node in visited:
            return
        visited.add(node)
        for child in graph.get(node, []):
            post_order_dfs(child)
        order.append(node)

    for node in graph:
        post_order_dfs(node)
    
    return order


def print_graph(graph):
    """Выводит граф в консоль."""
    for node, deps in graph.items():
        print(f"{node} -> {deps}")