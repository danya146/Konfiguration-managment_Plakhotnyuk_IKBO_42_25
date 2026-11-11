import argparse
import sys

def positive_int(value):
    """Валидатор для глубины анализа. Должно быть целое число > 0."""
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"Глубина должна быть больше 0, получено: {value}")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"Глубина должна быть целым числом, получено: {value}")

def create_parser():
    """Создает и настраивает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей для менеджера пакетов Python.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # 1. Имя анализируемого пакета
    parser.add_argument(
        "--package", "-p",
        type=str,
        required=True,
        help="Имя анализируемого пакета (например, requests)."
    )

    # 2. URL-адрес репозитория или путь к файлу
    parser.add_argument(
        "--repo",
        type=str,
        help="URL-адрес репозитория или путь к файлу тестового репозитория."
    )

    # 3. Режим работы с тестовым репозиторием
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Включить режим работы с тестовым репозиторием (локальный файл)."
    )

    # 4. Версия пакета
    parser.add_argument(
        "--version", "-v",
        type=str,
        default="latest",
        help="Версия анализируемого пакета."
    )

    # 5. Режим вывода в формате ASCII-дерева
    parser.add_argument(
        "--ascii-tree",
        action="store_true",
        help="Выводить зависимости в формате ASCII-дерева."
    )

    # 6. Максимальная глубина анализа
    parser.add_argument(
        "--depth", "-d",
        type=positive_int,
        default=3,
        help="Максимальная глубина анализа зависимостей."
    )

    # 7. Подстрока для фильтрации пакетов
    parser.add_argument(
        "--filter",
        type=str,
        default="",
        help="Подстрока для фильтрации пакетов."
    )

    return parser

def main():
    parser = create_parser()
    
    try:
        args = parser.parse_args()
    except SystemExit as e:
        sys.exit(e.code)

    print("=== Параметры запуска (Этап 1) ===")
    print(f"package: {args.package}")
    print(f"repo: {args.repo if args.repo else 'не задан'}")
    print(f"test_mode: {args.test_mode}")
    print(f"version: {args.version}")
    print(f"ascii_tree: {args.ascii_tree}")
    print(f"depth: {args.depth}")
    print(f"filter: {args.filter if args.filter else 'не задан'}")

if __name__ == "__main__":
    main()