import argparse
import sys
from graph_builder import build_graph, get_install_order
from visualizer import generate_plantuml, print_ascii_tree


def validate_depth(value):
    """Валидация максимальной глубины."""
    try:
        ivalue = int(value)
        if ivalue < 1:
            error_msg = f"Глубина должна быть > 0, получено: {value}"
            raise argparse.ArgumentTypeError(error_msg)
        return ivalue
    except ValueError:
        error_msg = f"Глубина должна быть числом, получено: {value}"
        raise argparse.ArgumentTypeError(error_msg)


def parse_args():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа (Этап 5)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--package", "-p", type=str, required=True,
        help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "--repo", "-r", type=str, required=True,
        help="URL-адрес или путь к файлу"
    )
    parser.add_argument(
        "--test-mode", "-t", action="store_true",
        help="Режим работы с тестовым репозиторием"
    )
    parser.add_argument(
        "--version", "-v", type=str, required=True,
        help="Версия пакета"
    )
    parser.add_argument(
        "--ascii-tree", "-a", action="store_true",
        help="Вывод в формате ASCII-дерева"
    )
    parser.add_argument(
        "--depth", "-d", type=validate_depth, default=3,
        help="Максимальная глубина анализа"
    )
    parser.add_argument(
        "--filter", "-f", type=str, default="",
        help="Подстрока для фильтрации пакетов"
    )
    return parser.parse_args()


def main():
    """Главная функция программы."""
    args = parse_args()

    print(f"Анализ пакета: {args.package}=={args.version}")
    print(f"Глубина: {args.depth} | Фильтр: '{args.filter}'")
    print(f"Тестовый режим: {args.test_mode}")
    print("-" * 40)

    try:
        graph = build_graph(
            package=args.package,
            version=args.version,
            repo_url=args.repo,
            max_depth=args.depth,
            filter_str=args.filter,
            test_mode=args.test_mode
        )

        if args.ascii_tree:
            print("Визуализация в формате ASCII-дерева:")
            print_ascii_tree(graph, args.package)
        else:
            print("Код PlantUML для визуализации:")
            uml = generate_plantuml(graph, args.package)
            print(uml)

        print("-" * 40)
        print("Порядок загрузки зависимостей:")
        install_order = get_install_order(graph)
        for i, pkg in enumerate(install_order, 1):
            print(f"{i}. {pkg}")

    except ValueError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
        sys.exit(1)