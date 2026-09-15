from worker import Worker

def input_user() -> Worker:
    """Запрос ввода данных от пользователя."""
    print("\n*** Ввод данных сотрудника ***")
    surname = input("Фамилия и инициалы: ").strip()
    position = input("Занимаемая должность: ").strip()

    while True:
        try:
            salary = float(input("Заработная плата в рублях: "))
            if salary < 0:
                print("Зарплата не может быть отрицательной. Повторите ввод.")
                continue
            break
        except ValueError:
            print("Ошибка ввода. Введите число.")

    while True:
        try:
            hire_year = int(input("Год поступления на работу: "))
            if not (1900 <= hire_year <= 2026):
                print("Год вне допустимого диапазона. Повторите ввод.")
                continue
            break
        except ValueError:
            print("Ошибка ввода. Введите целое число.")

    return Worker(surname, position, salary, hire_year)


def input_yes_no(prompt: str) -> bool:
    """
    Запрос ответа.
    Возвращает True, если выбран пункт 1, и False, если выбран пункт 2.
    """
    while True:
        print(f"\n{prompt}")
        print("1. Да")
        print("2. Нет")
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            return True
        if choice == "2":
            return False
        print("Некорректный ввод. Введите 1 или 2.")

# Функции вывода и выбора.
def print_workers(workers: list) -> None:
    """Вывод списка сотрудников в виде таблицы."""
    print("-" * 90)
    print(f"{'№':<4} | {'ФИО':<25} | {'Должность':<20} | {'Зарплата':>10} | {'Год'} | Стаж")
    print("-" * 90)
    for i, w in enumerate(workers, start=1):
        print(f"{i:<4} | {w.display()}")
    print("-" * 90)


def choose_worker(workers: list, action_name: str) -> int:
    """
    Вывод списка сотрудников и запрос № записи.
    Возврат индекса выбранного сотрудника или -1 при отмене.
    """
    if not workers:
        print(f"\nСписок сотрудников пуст. {action_name} невозможно.")
        return -1

    print(f"\n--- {action_name} ---")
    print_workers(workers)

    while True:
        try:
            raw = input(f"Введите номер сотрудника (1–{len(workers)}) "
                        f"или 0 для отмены: ").strip()
            num = int(raw)
            if num == 0:
                print("Операция отменена.")
                return -1
            if 1 <= num <= len(workers):
                return num - 1
            print(f"Введите число от 0 до {len(workers)}.")
        except ValueError:
            print("Ошибка ввода. Введите целое число.")

# Функции пунктов меню.
def menu_add(workers: list) -> None:
    """1: ввод данных нового сотрудника."""
    while True:
        workers.append(input_user())
        print("\nСотрудник успешно добавлен.")
        if not input_yes_no("Добавить ещё одного сотрудника?"):
            break


def menu_show(workers: list) -> None:
    """2: вывод таблицы со списком сотрудников."""
    if not workers:
        print("\nСписок сотрудников пуст.")
        return
    print("\nТекущий список сотрудников:")
    print_workers(workers)


def menu_edit(workers: list) -> None:
    """3: изменение данных сотрудника."""
    idx = choose_worker(workers, "Изменение данных")
    if idx == -1:
        return

    w = workers[idx]
    print(f"\nВыбран сотрудник: {w.get_surname()}")
    print("Какое поле необходимо изменить?")
    print("1. Фамилия и инициалы")
    print("2. Занимаемая должность")
    print("3. Заработная плата")
    print("4. Год поступления на работу")
    print("0. Отмена")

    while True:
        choice = input("Ваш выбор: ").strip()
        if choice == "0":
            print("Изменения отменены.")
            return
        if choice in ("1", "2", "3", "4"):
            break
        print("Некорректный ввод. Введите 0, 1, 2, 3 или 4.")

    try:
        if choice == "1":
            new_value = input("Новая фамилия и инициалы: ").strip()
            w.set_surname(new_value)
        elif choice == "2":
            new_value = input("Новая должность: ").strip()
            w.set_position(new_value)
        elif choice == "3":
            while True:
                try:
                    new_value = float(input("Новая заработная плата: "))
                    w.set_salary(new_value)
                    break
                except ValueError:
                    print("Введите число.")
        elif choice == "4":
            while True:
                try:
                    new_value = int(input("Новый год поступления: "))
                    w.set_hire_year(new_value)
                    break
                except ValueError:
                    print("Введите целое число.")
        print("Данные успешно обновлены.")
    except ValueError as e:
        print(f"Ошибка при изменении данных: {e}")


def menu_delete(workers: list) -> None:
    """4: удаление информации о сотруднике."""
    idx = choose_worker(workers, "Удаление сотрудника")
    if idx == -1:
        return

    w = workers[idx]
    print(f"\nВыбран сотрудник: {w.get_surname()}")
    if input_yes_no("Вы действительно хотите удалить эту запись?"):
        del workers[idx]
        print("Запись удалена.")
    else:
        print("Удаление отменено.")


def menu_filter(workers: list) -> None:
    """
    Фильтрация по стажу.
    Доступна из пункта 2.
    """
    if not workers:
        print("\nСписок сотрудников пуст.")
        return

    while True:
        try:
            min_exp = int(input("\nВведите значение стажа: "))
            if min_exp < 0:
                print("Значение не может быть отрицательным.")
                continue
            break
        except ValueError:
            print("Ошибка ввода. Введите целое число.")

    filtered = [w for w in workers if w.check_experience(min_exp)]
    print(f"\nСотрудники со стажем более {min_exp} лет:")
    if filtered:
        print_workers(filtered)
    else:
        print("Таких сотрудников нет.")

# Главное меню приложения.
def show_main_menu() -> None:
    """Вывод меню приложения."""
    print("\n" + "=" * 60)
    print(" ООО «Прибой» — учёт сотрудников")
    print("=" * 60)
    print("1. Ввести данные нового сотрудника")
    print("2. Вывести таблицу со списком сотрудников")
    print("3. Изменить данные сотрудника")
    print("4. Удалить информацию о сотруднике")
    print("5. Выйти из приложения")


def main() -> None:
    """Главная функция приложения."""
    workers: list[Worker] = []

    while True:
        show_main_menu()
        choice = input("\nВаш выбор (1–5): ").strip()

        if choice == "1":
            menu_add(workers)
        elif choice == "2":
            menu_show(workers)
            if workers:
                if input_yes_no("Выполнить фильтрацию по стажу?"):
                    menu_filter(workers)
        elif choice == "3":
            menu_edit(workers)
        elif choice == "4":
            menu_delete(workers)
        elif choice == "5":
            print("\nЗавершение работы приложения. Всего доброго!")
            break
        else:
            print("Некорректный ввод. Введите число от 1 до 5.")


if __name__ == "__main__":
    main()