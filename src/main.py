import argparse
import sys
import data_fetcher

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
    Добавляет базовые аргументы (пакет, версия, репозиторий).
    """
    parser.add_argument(
        "--package", "-p", type=str, required=True,
        help="Имя анализируемого пакета."
    )
    parser.add_argument(
        "--repo", type=str,
        help="URL или путь к файлу тестового репозитория."
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
        "--depth", "-d", type=positive_int, default=3,
        help="Максимальная глубина анализа."
    )
    parser.add_argument(
        "--filter", type=str, default="",
        help="Подстрока для фильтрации пакетов."
    )

def create_parser():
    """
    Создает и настраивает парсер аргументов командной строки.
    Возвращает объект ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    add_base_args(parser)
    add_visual_args(parser)
    return parser

def get_metadata(args):
    """
    Получает метаданные пакета в зависимости от режима работы.
    Возвращает строку метаданных или None.
    """
    if args.test_mode:
        if not args.repo:
            print("Ошибка: В режиме тестирования нужно указать --repo")
            return None
        print(f"[Тест] Чтение из файла: {args.repo}")
        return data_fetcher.fetch_from_file(args.repo)
    else:
        if not args.repo:
            print("Ошибка: Для реальных данных нужен --repo")
            return None
        print(f"[Реальный режим] Загрузка по URL: {args.repo}")
        return data_fetcher.fetch_from_url(args.repo)

def main():
    """
    Главная функция приложения.
    Парсит аргументы, получает метаданные и выводит зависимости.
    """
    parser = create_parser()
    try:
        args = parser.parse_args()
    except SystemExit as exit_code:
        sys.exit(exit_code.code)

    print(f"=== Пакет: {args.package} (Версия: {args.version}) ===")

    metadata = get_metadata(args)
    if metadata is None:
        print("Не удалось получить метаданные. Завершение работы.")
        sys.exit(1)

    dependencies = data_fetcher.extract_dependencies(metadata)

    if not dependencies:
        print("Прямые зависимости не найдены.")
    else:
        print(f"\nНайдено прямых зависимостей: {len(dependencies)}")
        for dep in dependencies:
            print(f"- {dep}")

if __name__ == "__main__":
    main()