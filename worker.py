import datetime

class Worker:
    """
    Класс описывает учётную карточку работника организации ООО "Прибой".
    Поля:
        surname - фамилия и инициалы;
        position - занимаемая должность;
        salary - заработная плата;
        hire_year - год поступления на работу.
    """
    def __init__(self, surname: str = "Не указано",
                 position: str = "Не указано",
                 salary: float = 0.0,
                 hire_year: int = 0):
        """
        Конструктор по умолчанию.        
        """
        self.__surname = surname
        self.__position = position
        self.__salary = float(salary)
        self.__hire_year = int(hire_year)

    @classmethod
    def from_line(cls, line: str) -> "Worker":
        """
        Альтернативный конструктор: создание объекта из строки вида
        'Фамилия И.О.; должность; зарплата; год'.
        """
        parts = [p.strip() for p in line.split(";")]
        if len(parts) != 4:
            raise ValueError("Ожидается 4 поля, разделённых ';'.")
        return cls(parts[0], parts[1], float(parts[2]), int(parts[3]))

    @classmethod
    def from_dict(cls, data: dict) -> "Worker":
        """
        Альтернативный конструктор: создание объекта из словаря.
        """
        return cls(
            surname=data.get("surname", "Не указано"),
            position=data.get("position", "Не указано"),
            salary=data.get("salary", 0.0),
            hire_year=data.get("hire_year", 0),
        )
    
    def __del__(self):
        """
        Деструктор.
        """
        print(f"[деструктор] Объект Worker '{self.__surname}' удалён.")

    #Методы изменения полей.

    def set_surname(self, surname: str) -> None:
        self.__surname = surname

    def set_position(self, position: str) -> None:
        self.__position = position

    def set_salary(self, salary: float) -> None:
        if salary < 0:
            raise ValueError("Зарплата не может быть отрицательной.")
        self.__salary = float(salary)

    def set_hire_year(self, hire_year: int) -> None:
        current_year = datetime.datetime.now().year
        if not (1900 <= hire_year <= current_year):
            raise ValueError("Год поступления вне допустимого диапазона.")
        self.__hire_year = int(hire_year)

    #Методы получения полей.

    def get_surname(self) -> str:
        return self.__surname

    def get_position(self) -> str:
        return self.__position

    def get_salary(self) -> float:
        return self.__salary

    def get_hire_year(self) -> int:
        return self.__hire_year

    #Методы расчёта.

    def get_experience(self) -> int:
        """Возврат стажа работы в организации."""
        current_year = datetime.datetime.now().year
        if self.__hire_year == 0:
            return 0
        return current_year - self.__hire_year

    def check_experience(self, min_experience: int) -> bool:
        """Проверка превышения заданного значения стажем."""
        return self.get_experience() > min_experience

    #Методы отображения.

    def display(self) -> str:
        """Возврат строковго представления объекта."""
        return (f"{self.__surname:<25} | {self.__position:<20} | "
                f"{self.__salary:>10.2f} | {self.__hire_year} | "
                f"стаж: {self.get_experience()}")

    def __str__(self) -> str:
        return self.display()

    def __repr__(self) -> str:
        return (f"Worker(surname='{self.__surname}', "
                f"position='{self.__position}', "
                f"salary={self.__salary}, "
                f"hire_year={self.__hire_year})")