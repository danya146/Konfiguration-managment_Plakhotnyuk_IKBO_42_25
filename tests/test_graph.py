import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'src')
))
import graph_builder

class TestGraphBuilder(unittest.TestCase):
    """
    Тесты для модуля построения графа зависимостей.
    """

    def setUp(self):
        """Создаем тестовый граф перед каждым тестом."""
        self.graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": ["E"],
            "E": []
        }
        self.cyclic_graph = {
            "X": ["Y"],
            "Y": ["X"]
        }

    def test_build_tree_depth(self):
        """Тест: проверка ограничения глубины."""
        tree = graph_builder.build_tree("A", self.graph, 1, "")
        self.assertIn("A", tree)
        self.assertIn("B", tree["A"])
        self.assertIn("C", tree["A"])
        self.assertEqual(tree["A"]["B"], {})

    def test_filter(self):
        """Тест: проверка фильтрации пакетов."""
        tree = graph_builder.build_tree("A", self.graph, 5, "B")
        self.assertNotIn("B", tree["A"])
        self.assertIn("C", tree["A"])

    def test_cycle_detection(self):
        """Тест: проверка обнаружения цикла."""
        tree = graph_builder.build_tree("X", self.cyclic_graph, 5, "")
        # Превращаем весь словарь в строку и ищем маркер цикла
        tree_str = str(tree)
        self.assertIn("[CYCLE]", tree_str)

    def test_load_order_dag(self):
        """Тест: проверка топологической сортировки (без циклов)."""
        order = graph_builder.get_load_order("A", self.graph)
        self.assertEqual(order[0], "E")
        self.assertEqual(order[-1], "A")

    def test_load_order_cycle(self):
        """Тест: топологическая сортировка при наличии цикла."""
        order = graph_builder.get_load_order("X", self.cyclic_graph)
        self.assertIsNone(order)

if __name__ == '__main__':
    unittest.main()