def generate_plantuml(tree):
    """
    Генерирует код PlantUML на основе вложенного словаря графа.
    Возвращает строку с кодом диаграммы.
    """
    lines = ["@startuml", "skinparam linetype ortho"]
    
    def traverse(node, parent=None):
        """Рекурсивно обходит дерево и создает связи."""
        for pkg, children in node.items():
            if pkg == "[CYCLE]":
                continue
                
            if parent:
                lines.append(f"{parent} --> {pkg}")
                
            if children:
                traverse(children, pkg)

    traverse(tree)
    lines.append("@enduml")
    return "\n".join(lines)