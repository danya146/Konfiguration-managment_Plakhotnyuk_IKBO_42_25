def generate_plantuml(graph, package_name):
    """Генерирует текст PlantUML для графа."""
    lines = ["@startuml"]
    lines.append(f"title Dependency graph for {package_name}")
    
    for node, deps in graph.items():
        for dep in deps:
            lines.append(f'"{node}" --> "{dep}"')
            
    lines.append("@enduml")
    return "\n".join(lines)


def print_ascii_tree(graph, root, prefix="", visited=None):
    """Рекурсивно выводит граф в виде ASCII-дерева."""
    if visited is None:
        visited = set()
    
    if root in visited:
        print(f"{prefix}└── {root} (cycle)")
        return
    
    visited.add(root)
    print(f"{prefix}└── {root}")
    
    deps = graph.get(root, [])
    for i, dep in enumerate(deps):
        is_last = (i == len(deps) - 1)
        if is_last:
            new_prefix = prefix + "    "
        else:
            new_prefix = prefix + "│   "
        
        if dep in graph:
            print_ascii_tree(graph, dep, new_prefix, visited)
        else:
            print(f"{new_prefix}└── {dep}")