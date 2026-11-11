import argparse
import sys
import data_fetcher
import graph_builder
import visualizer

def positive_int(value):
    """
    Валидатор для глубины анализа.
    Проверяет, что введено целое число > 0.
    """
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(
                f"Глубина должна быть больше 0, получено: {value}"
            )
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Глубина должна быть целым числом, получено: {value}"
        )

def add_base_args(parser):
    """
    Добавляет базовые аргументы.
    """
    parser.add_argument(
        "--package", "-p", type=str, required=True,
        help="Имя анализируемого пакета."
    )
    parser.add_argument(
        "--repo", type=str,
        help="URL или путь к файлу."
    )
    parser.add_argument(
        "--test-mode", action="store_true",
        help="Режим тестового репозитория."
    )
    parser.add_argument(
        "--version", "-v", type=str, default="latest",
        help="Версия пакета."
    )

def add_visual_args(parser):
    """
    Добавляет аргументы для визуализации и фильтрации.
    """
    parser.add_argument(
        "--ascii-tree", action="store_true",
        help="Вывод в формате ASCII-дерева."
    )
    parser.add_argument(
        "--plantuml", action="store_true",
        help="Вывод в формате PlantUML."
    )
    parser.add_argument(
        "--output", type=str, default="graph.puml",
        help="Путь для сохранения файла PlantUML."
    )
    parser.add_argument(
        "--depth", "-d", type=positive_int, default=3,
        help="Максимальная глубина."
    )
    parser.add_argument(
        "--filter", type=str, default="",
        help="Подстрока для фильтрации."
    )
    parser.add_argument(
        "--load-order", action="store_true",
        help="Порядок загрузки."
    )

def create_parser():
    """
    Создает и настраивает парсер.
    """
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    add_base_args(parser)
    add_visual_args(parser)
    return parser

def print_tree(tree, indent=0):
    """
    Выводит дерево в консоль.
    """
    for pkg, children in tree.items():
        if pkg == "[CYCLE]":
            print("  " * indent + "└── [Обнаружен цикл]")
            continue
        print("  " * indent + "├── " + pkg)
        if children:
            print_tree(children, indent + 1)

def main():
    """
    Главная функция.
    """
    parser = create_parser()
    try:
        args = parser.parse_args()
    except SystemExit as exit_code:
        sys.exit(exit_code.code)

    print(f"=== Пакет: {args.package} (Версия: {args.version}) ===")

    if args.test_mode:
        if not args.repo:
            print("Ошибка: Нужен --repo с путем к файлу графа.")
            sys.exit(1)
        print(f"[Тест] Чтение графа из: {args.repo}")
        graph = graph_builder.parse_test_graph(args.repo)
        
        if not graph:
            print("Ошибка: Тестовый граф пуст или не найден.")
            sys.exit(1)

        if args.load_order:
            print("\nВычисление порядка загрузки зависимостей...")
            order = graph_builder.get_load_order(
                args.package.upper(), graph
            )
            if order:
                print("Порядок загрузки (от зависимостей к корню):")
                for i, pkg in enumerate(order, 1):
                    print(f"{i}. {pkg}")
            else:
                print("Не удалось вычислить порядок из-за цикла.")
            sys.exit(0)
            
        tree = graph_builder.build_tree(
            args.package.upper(), graph, args.depth, args.filter
        )
        
        if args.plantuml:
            print("\nКод PlantUML для графа зависимостей:")
            print(visualizer.generate_plantuml(tree))
            if visualizer.save_plantuml_to_file(tree, args.output):
                print(f"\n[Успех] Диаграмма сохранена в файл: {args.output}")
        else:
            print("\nГраф зависимостей (DFS):")
            print_tree(tree)
    else:
        print("Реальный режим (интернет) пока не реализован.")
        sys.exit(0)

if __name__ == "__main__":
    main()