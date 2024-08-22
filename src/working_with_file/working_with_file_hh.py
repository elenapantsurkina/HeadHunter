import json
from src.working_with_file.working_with_file_base import VacancyRepository

from src.vacancies import Vacancies
from src.api.api_hh import HHJobAPI


class JsonVacancyRepository(VacancyRepository):
    """Класс работы с файлами"""
    file = "vacancies.json"

    def __init__(self, file_path=file):
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
        with open(self.file_path, 'w+', encoding='utf-8') as f:
            for v in vacancies:
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

    def delete_vacancy(self):
        """Удаляем вакансию """
        with open(self.file_path, 'w+', encoding='utf-8') as f:
            pass


# Пример использования
if __name__ == "__main__":
    hh_api = HHJobAPI()
    hh_api.connect()
    repository = JsonVacancyRepository()

    # Пример добавления вакансий
    new_vacancy = {
        "id": 1,
        "name": "Программист Python",
        "url": "https://example.com/vacancy1",
        "salary": 60000,
        "description": "Разработка приложений на Python."
    }
    repository.add_vacancy(new_vacancy)

    # Пример получения вакансий
    criteria = {"name": "Программист Python"}
    vacancies = repository.get_vacancies(criteria)
    print(vacancies)
