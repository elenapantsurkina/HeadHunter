from abc import ABC, abstractmethod
import requests


class AbstractAPI(ABC):
    @abstractmethod
    def connect(self):
        """Подключение к API."""
        pass

    @abstractmethod
    def get_vacancies(self, query, area=None, page=0):
        """Получение вакансий по запросу.

        :param query: Запрос для поиска вакансий.
        :param area: ID региона для поиска (опционально).
        :param page: Номер страницы результата (опционально).
        :return: Список вакансий.
        """
        pass


class HHJobAPI(AbstractAPI):
    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.session = requests.Session()

    def connect(self):
        """Проверка подключения к API.
        Для этого делаем простой запрос к API (например, к эндпоинту вакансий).
        """
        response = self.session.get(self.BASE_URL)
        if response.status_code == 200:
            print("Успешно подключено к hh.ru API")
        else:
            print("Не удалось подключиться к hh.ru API")
            response.raise_for_status()

    def get_vacancies(self, query, area=None, page=0):
        """Получение списка вакансий по заданному запросу."""
        params = {
            'text': query,
            'area': area,
            'page': page
        }
        response = self.session.get(self.BASE_URL, params=params)
        if response.status_code == 200:
            vacancies = response.json().get('items', [])
            return vacancies
        else:
            print("Ошибка при получении вакансий:", response.status_code)
            response.raise_for_status()

    @abstractmethod
    def clear(self):
        """Очистка файла от содержимого"""
        pass


# Пример использования
if __name__ == "__main__":
    hh_api = HHJobAPI()
    hh_api.connect()  # Проверка подключения

    # Запрос вакансий
    vacancies = hh_api.get_vacancies("python developer", area=1)  # Поиск по всей России
    for vacancy in vacancies:
        print(vacancy['name'], vacancy['area']['name'])
