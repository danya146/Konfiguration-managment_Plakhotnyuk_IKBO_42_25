@echo off
chcp 65001 >nul
echo ТЕСТ 1 (Этап 1): Обработка ошибок
python src\main.py -p "A" -r "test_repo.json" -v "1.0" -t -d "abc"
echo.
echo ТЕСТ 2 (Этап 2): Сбор данных с PyPI
python src\main.py -p "requests" -r "https://pypi.org" -v "2.31.0" -d 1
echo.
echo ТЕСТ 3 (Этап 3): DFS, тестовый режим и фильтр
python src\main.py -p "A" -r "test_repo.json" -v "1.0" -t -d 5 -f "C"
echo.
echo ТЕСТ 4 (Этап 4): Порядок загрузки
python src\main.py -p "B" -r "test_repo.json" -v "1.0" -t -d 5
echo.
echo ТЕСТ 5 (Этап 5): Визуализация (ASCII-дерево)
python src\main.py -p "A" -r "test_repo.json" -v "1.0" -t -d 5 -a
echo.
pause