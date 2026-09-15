from worker import Worker

def input_user() -> Worker:
    """Запрос ввода от пользователя."""
    print("\nВвод данных сотрудника")
    surname = input("Фамилия и инициалы: ").strip()
    position = input("Занимаемая должность: ").strip()

    while True:
        try:
            salary = float(input("Заработная плата (руб.): "))
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

def print_workers(workers: list) -> None:
    """Вывод списка сотрудников в таблицу."""
    print("-" * 90)
    print(f"{'ФИО':<25} | {'Должность':<20} | {'Зарплата':>10} | {'Год'} | Стаж")
    print("-" * 90)
    for w in workers:
        print(w.display())
    print("-" * 90)

def main() -> None:
    print("=" * 60)
    print(" ООО «Прибой» - учёт сотрудников")
    print("=" * 60)

    workers: list[Worker] = []

    # Ввод данных работников
    while True:
        workers.append(input_user())
        cont = input("\nДобавить ещё одного сотрудника? (y/n): ").strip().lower()
        if cont != "y":
            break

    print("\nВведённый список сотрудников:")
    print_workers(workers)

    # Запрос стажа
    while True:
        try:
            min_exp = int(input("\nВведите значение стажа: "))
            if min_exp < 0:
                print("Значение не может быть отрицательным.")
                continue
            break
        except ValueError:
            print("Ошибка ввода. Введите целое число.")

    # Фильтрация работников по стажу
    filtered = [w for w in workers if w.check_experience(min_exp)]

    print(f"\Сотрудники со стажем более {min_exp} лет:")
    if filtered:
        print_workers(filtered)
    else:
        print("Таких сотрудников нет.")


if __name__ == "__main__":
    main()