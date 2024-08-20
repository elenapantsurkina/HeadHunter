
import json
from abc import ABC, abstractmethod


class VacancyRepository(ABC):
    """Создаем абстрактный класс для реализации методов создания добавления и удаления вакансий """
    @abstractmethod
    def add_vacancy(self, vacancy):
        """Добавить вакансию в файл."""
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        """Получить вакансии по заданным критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        """Удалить вакансию по идентификатору."""
        pass


class JsonVacancyRepository(VacancyRepository):
    def __init__(self, file_path):
        self.file_path = file_path

    def _load_data(self):
        """Считывает данные из файла."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_data(self, vacancies):
        """Сохраняет данные в файл."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy):
        """Добавляем вакансию в файл."""
        vacancies = self._load_data()
        vacancies.append(vacancy)
        self._save_data(vacancies)

    def get_vacancies(self, criteria):
        """Получаем вакансии по заданным критериям."""
        vacancies = self._load_data()
        return [vacancy for vacancy in vacancies if all(item in vacancy.items() for item in criteria.items())]

    def delete_vacancy(self, vacancy_id):
        """Удаляем вакансию по идентификатору."""
        vacancies = self._load_data()
        vacancies = [vacancy for vacancy in vacancies if vacancy.get('id') != vacancy_id]
        self._save_data(vacancies)


# Пример использования
if __name__ == "__main__":
    repository = JsonVacancyRepository("vacancies.json")

    # Пример добавления вакансий
    new_vacancy = {
        "id": 1,
        "title": "Программист Python",
        "url": "https://example.com/vacancy1",
        "salary": 60000,
        "description": "Разработка приложений на Python."
    }
    repository.add_vacancy(new_vacancy)

    # Пример получения вакансий
    criteria = {"name": "Программист Python"}
    vacancies = repository.get_vacancies(criteria)
    print(vacancies)

    # Пример удаления вакансии
    repository.delete_vacancy(1)
    