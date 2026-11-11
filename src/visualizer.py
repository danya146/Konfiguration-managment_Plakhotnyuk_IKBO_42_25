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

def save_plantuml_to_file(tree, filepath):
    """
    Сохраняет код PlantUML в файл.
    Возвращает True в случае успеха, иначе False.
    """
    code = generate_plantuml(tree)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        return True
    except Exception as error:
        print(f"Ошибка при сохранении файла: {error}")
        return False