import unittest
from unittest.mock import patch
from io import StringIO
import datetime

from worker import Worker
from main import (
    input_user,
    input_yes_no,
    print_workers,
    choose_worker,
    menu_add,
    menu_show,
    menu_edit,
    menu_delete,
    menu_filter,
)

# Раздел 1. Тесты класса Worker
class TestWorker(unittest.TestCase):
    """Набор тестов для класса Worker."""

    def test_default_constructor(self):
        """Проверка конструктора по умолчанию."""
        w = Worker()
        self.assertEqual(w.get_surname(), "Не указано")
        self.assertEqual(w.get_position(), "Не указано")
        self.assertEqual(w.get_salary(), 0.0)
        self.assertEqual(w.get_hire_year(), 0)

    def test_parameterized_constructor(self):
        """Проверка конструктора с параметрами."""
        w = Worker("Иванов И.И.", "Инженер", 95000.0, 2015)
        self.assertEqual(w.get_surname(), "Иванов И.И.")
        self.assertEqual(w.get_position(), "Инженер")
        self.assertEqual(w.get_salary(), 95000.0)
        self.assertEqual(w.get_hire_year(), 2015)

    def test_from_line_constructor(self):
        """Проверка альтернативного конструктора из строки."""
        w = Worker.from_line("Петров П.П.; Администратор; 80000; 2020")
        self.assertEqual(w.get_surname(), "Петров П.П.")
        self.assertEqual(w.get_salary(), 80000.0)

    def test_from_dict_constructor(self):
        """Проверка альтернативного конструктора из словаря."""
        data = {"surname": "Сидорова А.В.", "position": "Аналитик",
                "salary": 110000, "hire_year": 2010}
        w = Worker.from_dict(data)
        self.assertEqual(w.get_surname(), "Сидорова А.В.")
        self.assertEqual(w.get_hire_year(), 2010)

    def test_setters_validation(self):
        """Проверка валидации в сеттерах."""
        w = Worker()
        with self.assertRaises(ValueError):
            w.set_salary(-1000)
        with self.assertRaises(ValueError):
            w.set_hire_year(1800)
        with self.assertRaises(ValueError):
            w.set_hire_year(2100)

    def test_setters_change_values(self):
        """Проверка изменения значений через сеттеры (используется в menu_edit)."""
        w = Worker()
        w.set_surname("Тестов Т.Т.")
        w.set_position("Тестировщик")
        w.set_salary(50000)
        w.set_hire_year(2020)
        self.assertEqual(w.get_surname(), "Тестов Т.Т.")
        self.assertEqual(w.get_position(), "Тестировщик")
        self.assertEqual(w.get_salary(), 50000.0)
        self.assertEqual(w.get_hire_year(), 2020)

    def test_experience_calculation(self):
        """Проверка расчёта стажа."""
        current_year = datetime.datetime.now().year
        w = Worker("Тестов Т.Т.", "Тестировщик", 50000, current_year - 5)
        self.assertEqual(w.get_experience(), 5)

    def test_check_experience(self):
        """Проверка метода check_experience (используется в menu_filter)."""
        w = Worker("Тестов Т.Т.", "Тестировщик", 50000, 2015)
        self.assertTrue(w.check_experience(5))
        self.assertFalse(w.check_experience(50))

    def test_str_representation(self):
        """Проверка строкового представления (используется в print_workers)."""
        w = Worker("Иванов И.И.", "Инженер", 95000, 2015)
        s = str(w)
        self.assertIn("Иванов И.И.", s)
        self.assertIn("Инженер", s)
        self.assertIn("95000", s)

    def test_delete_from_list(self):
        """Проверка удаления объекта из списка (имитация menu_delete)."""
        workers = [
            Worker("Иванов И.И.", "Инженер", 95000, 2015),
            Worker("Петров П.П.", "Администратор", 80000, 2023),
        ]
        self.assertEqual(len(workers), 2)
        del workers[0]
        self.assertEqual(len(workers), 1)
        self.assertEqual(workers[0].get_surname(), "Петров П.П.")


# Раздел 2. Тесты функций интерактивного меню
class TestMenuFunctions(unittest.TestCase):
    """Набор тестов для функций интерактивного меню модуля main.py."""
    
    # Тесты функции input_yes_no    
    @patch("builtins.input", side_effect=["1"])
    def test_input_yes_no_returns_true(self, mock_input):
        """Проверка возврата True при выборе '1. Да'."""
        result = input_yes_no("Тестовый вопрос?")
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["2"])
    def test_input_yes_no_returns_false(self, mock_input):
        """Проверка возврата False при выборе '2. Нет'."""
        result = input_yes_no("Тестовый вопрос?")
        self.assertFalse(result)

    @patch("builtins.input", side_effect=["3", "abc", "1"])
    def test_input_yes_no_invalid_then_valid(self, mock_input):
        """Проверка повторного запроса при некорректном вводе."""
        result = input_yes_no("Тестовый вопрос?")
        self.assertTrue(result)
        self.assertEqual(mock_input.call_count, 3)

    # Тесты функции input_user
    @patch("builtins.input", side_effect=[
        "Иванов И.И.",
        "Инженер",
        "95000",
        "2015",
    ])
    def test_input_user_valid(self, mock_input):
        """Проверка корректного ввода данных сотрудника."""
        w = input_user()
        self.assertEqual(w.get_surname(), "Иванов И.И.")
        self.assertEqual(w.get_position(), "Инженер")
        self.assertEqual(w.get_salary(), 95000.0)
        self.assertEqual(w.get_hire_year(), 2015)

    @patch("builtins.input", side_effect=[
        "Петров П.П.",
        "Администратор",
        "-100",       # некорректная зарплата
        "abc",        # не число
        "80000",      # корректная зарплата
        "1800",       # некорректный год
        "xyz",        # не число
        "2020",       # корректный год
    ])
    def test_input_user_with_invalid_then_valid(self, mock_input):
        """Проверка обработки некорректного ввода с повторным запросом."""
        w = input_user()
        self.assertEqual(w.get_surname(), "Петров П.П.")
        self.assertEqual(w.get_salary(), 80000.0)
        self.assertEqual(w.get_hire_year(), 2020)
    
    # Тесты функции print_workers
    @patch("sys.stdout", new_callable=StringIO)
    def test_print_workers_with_numbering(self, mock_stdout):
        """Проверка вывода таблицы с нумерацией строк."""
        workers = [
            Worker("Иванов И.И.", "Инженер", 95000, 2015),
            Worker("Петров П.П.", "Администратор", 80000, 2023),
        ]
        print_workers(workers)
        output = mock_stdout.getvalue()
        self.assertIn("№", output)
        self.assertIn("1", output)
        self.assertIn("2", output)
        self.assertIn("Иванов И.И.", output)
        self.assertIn("Петров П.П.", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_workers_empty_list(self, mock_stdout):
        """Проверка вывода при пустом списке."""
        print_workers([])
        output = mock_stdout.getvalue()
        # Должны быть только разделители, без строк сотрудников
        self.assertIn("-" * 90, output)
    
    # Тесты функции choose_worker
    @patch("builtins.input", side_effect=["1"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_choose_worker_valid(self, mock_stdout, mock_input):
        """Проверка выбора сотрудника по номеру."""
        workers = [
            Worker("Иванов И.И.", "Инженер", 95000, 2015),
            Worker("Петров П.П.", "Администратор", 80000, 2023),
        ]
        idx = choose_worker(workers, "Тест")
        self.assertEqual(idx, 0)

    @patch("builtins.input", side_effect=["0"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_choose_worker_cancel(self, mock_stdout, mock_input):
        """Проверка отмены операции вводом '0'."""
        workers = [Worker("Иванов И.И.", "Инженер", 95000, 2015)]
        idx = choose_worker(workers, "Тест")
        self.assertEqual(idx, -1)

    @patch("builtins.input", side_effect=["5", "abc", "2"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_choose_worker_invalid_then_valid(self, mock_stdout, mock_input):
        """Проверка повторного запроса при некорректном номере."""
        workers = [
            Worker("Иванов И.И.", "Инженер", 95000, 2015),
            Worker("Петров П.П.", "Администратор", 80000, 2023),
        ]
        idx = choose_worker(workers, "Тест")
        self.assertEqual(idx, 1)

    @patch("sys.stdout", new_callable=StringIO)
    def test_choose_worker_empty_list(self, mock_stdout):
        """Проверка обработки пустого списка."""
        idx = choose_worker([], "Тест")
        self.assertEqual(idx, -1)
        output = mock_stdout.getvalue()
        self.assertIn("пуст", output.lower())
    
    # Тесты функции menu_add
    @patch("builtins.input", side_effect=[
        "Иванов И.И.", "Инженер", "95000", "2015",      # первый сотрудник
        "2",                                            # не добавлять ещё
    ])
    def test_menu_add_single(self, mock_input):
        """Проверка добавления одного сотрудника."""
        workers = []
        menu_add(workers)
        self.assertEqual(len(workers), 1)
        self.assertEqual(workers[0].get_surname(), "Иванов И.И.")

    @patch("builtins.input", side_effect=[
        "Иванов И.И.", "Инженер", "95000", "2015",          # первый
        "1",                                                # добавить ещё
        "Петров П.П.", "Администратор", "80000", "2023",    # второй
        "2",                                                # не добавлять ещё
    ])
    def test_menu_add_multiple(self, mock_input):
        """Проверка добавления нескольких сотрудников."""
        workers = []
        menu_add(workers)
        self.assertEqual(len(workers), 2)
        self.assertEqual(workers[0].get_surname(), "Иванов И.И.")
        self.assertEqual(workers[1].get_surname(), "Петров П.П.")
    
    # Тесты функции menu_show
    @patch("builtins.input", side_effect=["2"])  # не выполнять фильтрацию
    @patch("sys.stdout", new_callable=StringIO)
    def test_menu_show_with_data(self, mock_stdout, mock_input):
        """Проверка вывода списка сотрудников."""
        workers = [Worker("Иванов И.И.", "Инженер", 95000, 2015)]
        menu_show(workers)
        output = mock_stdout.getvalue()
        self.assertIn("Иванов И.И.", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_menu_show_empty(self, mock_stdout):
        """Проверка вывода при пустом списке."""
        workers = []
        menu_show(workers)
        output = mock_stdout.getvalue()
        self.assertIn("пуст", output.lower())
    
    # Тесты функции menu_edit
    @patch("builtins.input", side_effect=[
        "1",      # выбрать первого сотрудника
        "3",      # изменить зарплату
        "120000", # новое значение
    ])
    def test_menu_edit_salary(self, mock_input):
        """Проверка изменения зарплаты сотрудника."""
        workers = [Worker("Иванов И.И.", "Инженер", 95000, 2015)]
        menu_edit(workers)
        self.assertEqual(workers[0].get_salary(), 120000.0)

    @patch("builtins.input", side_effect=[
        "1",      # выбрать первого сотрудника
        "1",      # изменить фамилию
        "Сидоров С.С.",
    ])
    def test_menu_edit_surname(self, mock_input):
        """Проверка изменения фамилии сотрудника."""
        workers = [Worker("Иванов И.И.", "Инженер", 95000, 2015)]
        menu_edit(workers)
        self.assertEqual(workers[0].get_surname(), "Сидоров С.С.")

    @patch("builtins.input", side_effect=[
        "0",      # отмена выбора
    ])
    def test_menu_edit_cancel(self, mock_input):
        """Проверка отмены операции изменения."""
        workers = [Worker("Иванов И.И.", "Инженер", 95000, 2015)]
        menu_edit(workers)
        # Данные не должны измениться
        self.assertEqual(workers[0].get_salary(), 95000.0)

    @patch("sys.stdout", new_callable=StringIO)
    def test_menu_edit_empty_list(self, mock_stdout):
        """Проверка обработки пустого списка при изменении."""
        workers = []
        menu_edit(workers)
        output = mock_stdout.getvalue()
        self.assertIn("пуст", output.lower())
    
    # Тесты функции menu_delete
    @patch("builtins.input", side_effect=[
        "1",      # выбрать первого сотрудника
        "1",      # подтвердить удаление
    ])
    def test_menu_delete_confirm(self, mock_input):
        """Проверка удаления сотрудника с подтверждением."""
        workers = [
            Worker("Иванов И.И.", "Инженер", 95000, 2015),
            Worker("Петров П.П.", "Администратор", 80000, 2023),
        ]
        menu_delete(workers)
        self.assertEqual(len(workers), 1)
        self.assertEqual(workers[0].get_surname(), "Петров П.П.")

    @patch("builtins.input", side_effect=[
        "1",      # выбрать первого сотрудника
        "2",      # отменить удаление
    ])
    def test_menu_delete_cancel(self, mock_input):
        """Проверка отмены удаления."""
        workers = [
            Worker("Иванов И.И.", "Инженер", 95000, 2015),
            Worker("Петров П.П.", "Администратор", 80000, 2023),
        ]
        menu_delete(workers)
        self.assertEqual(len(workers), 2)

    @patch("builtins.input", side_effect=["0"])  # отмена выбора
    def test_menu_delete_cancel_choice(self, mock_input):
        """Проверка отмены на этапе выбора сотрудника."""
        workers = [Worker("Иванов И.И.", "Инженер", 95000, 2015)]
        menu_delete(workers)
        self.assertEqual(len(workers), 1)
    
    # Тесты функции menu_filter
    @patch("builtins.input", side_effect=["5"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_menu_filter_with_results(self, mock_stdout, mock_input):
        """Проверка фильтрации с наличием подходящих сотрудников."""
        workers = [
            Worker("Иванов И.И.", "Инженер", 95000, 2015),
            Worker("Петров П.П.", "Администратор", 80000, 2023),
        ]
        menu_filter(workers)
        output = mock_stdout.getvalue()
        self.assertIn("Иванов И.И.", output)
        self.assertNotIn("Петров П.П.", output)

    @patch("builtins.input", side_effect=["50"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_menu_filter_no_results(self, mock_stdout, mock_input):
        """Проверка фильтрации без подходящих сотрудников."""
        workers = [
            Worker("Иванов И.И.", "Инженер", 95000, 2015),
            Worker("Петров П.П.", "Администратор", 80000, 2023),
        ]
        menu_filter(workers)
        output = mock_stdout.getvalue()
        self.assertIn("нет", output.lower())

    @patch("builtins.input", side_effect=["-5", "abc", "5"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_menu_filter_invalid_then_valid(self, mock_stdout, mock_input):
        """Проверка обработки некорректного ввода стажа."""
        workers = [Worker("Иванов И.И.", "Инженер", 95000, 2015)]
        menu_filter(workers)
        # Функция должна завершиться без исключений
        self.assertEqual(mock_input.call_count, 3)

    @patch("sys.stdout", new_callable=StringIO)
    def test_menu_filter_empty_list(self, mock_stdout):
        """Проверка обработки пустого списка при фильтрации."""
        workers = []
        menu_filter(workers)
        output = mock_stdout.getvalue()
        self.assertIn("пуст", output.lower())



# Раздел 3. Интеграционные тесты
class TestIntegration(unittest.TestCase):
    """Интеграционные тесты, проверяющие совместную работу функций."""

    @patch("builtins.input", side_effect=[
        "Иванов И.И.", "Инженер", "95000", "2015",      # добавить сотрудника
        "2",                                            # не добавлять ещё
    ])
    def test_add_then_edit(self, mock_input):
        """Проверка последовательности добавления и изменения."""
        workers = []
        menu_add(workers)
        self.assertEqual(len(workers), 1)

        # Имитация изменения зарплаты через меню
        with patch("builtins.input", side_effect=["1", "3", "120000"]):
            menu_edit(workers)
        self.assertEqual(workers[0].get_salary(), 120000.0)

    @patch("builtins.input", side_effect=[
        "Иванов И.И.", "Инженер", "95000", "2015",
        "1",
        "Петров П.П.", "Администратор", "80000", "2023",
        "2",
    ])
    def test_add_multiple_then_delete(self, mock_input):
        """Проверка добавления нескольких и удаления одного."""
        workers = []
        menu_add(workers)
        self.assertEqual(len(workers), 2)

        with patch("builtins.input", side_effect=["1", "1"]):
            menu_delete(workers)
        self.assertEqual(len(workers), 1)
        self.assertEqual(workers[0].get_surname(), "Петров П.П.")

    @patch("builtins.input", side_effect=[
        "Иванов И.И.", "Инженер", "95000", "2015",
        "1",
        "Петров П.П.", "Администратор", "80000", "2023",
        "2",
    ])
    def test_add_then_filter(self, mock_input):
        """Проверка добавления и последующей фильтрации."""
        workers = []
        menu_add(workers)

        with patch("builtins.input", side_effect=["5"]), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            menu_filter(workers)
            output = mock_stdout.getvalue()
            self.assertIn("Иванов И.И.", output)
            self.assertNotIn("Петров П.П.", output)


if __name__ == "__main__":
    unittest.main()