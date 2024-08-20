
class Vacancies:
    """Класс для работы с вакансиями"""
    def __init__(self, name, id, salary, description, url):
        self.name = name
        self.id = id
        self.salary = salary if salary is not None else "Зарплата не указана"
        self.description = description
        self.url = url

        __slots__ = ("name", "id", "salary", "description, url")

    def validate(self):
        # Проверяем, указан ли заголовок вакансии
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Название вакансии должно быть непустой строкой.")

        # Проверяем, указана ли ссылка на вакансию
        if not isinstance(self.url, str) or not self.url.strip():
            raise ValueError("Ссылка на вакансию должна быть непустой строкой.")

        # Проверяем зарплату
        if isinstance(self.salary, (int, float)) and self.salary < 0:
            raise ValueError("Зарплата не может быть отрицательной.")
        elif not isinstance(self.salary, (int, float, str)):
            raise ValueError("Зарплата должна быть числом или строкой 'Зарплата не указана'.")

    def __eq__(self, other):
        if not isinstance(other, Vacancies):
            return NotImplemented
        return self.salary == other.salary

    def __lt__(self, other):
        if not isinstance(other, Vacancies):
            return NotImplemented
        if isinstance(self.salary, (int, float)) and isinstance(other.salary, (int, float)):
            return self.salary < other.salary
        return False

    def __repr__(self):
        return f"Vacancy(name='{self.name}', url='{self.url}', salary={self.salary}, description='{self.description}')"