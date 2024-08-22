from src.api.api_base import AbstractAPI
import requests
from src.vacancies import Vacancies


class HHJobAPI(AbstractAPI):
    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.__session = requests.Session()
        self.__vacancies = []
        self.__vacancies_new = []

    def connect(self):
        """Проверка подключения к API.
        делаем простой запрос к API
        """
        response = self.__session.get(self.BASE_URL)
        if response.status_code == 200:
            print("Успешно подключено к hh.ru API")
        else:
            print("Не удалось подключиться к hh.ru API")
            response.raise_for_status()

    def get_vacancies(self, query, area=None, page=20):
        """Получение списка вакансий по заданному запросу."""
        params = {
            'text': query,
            'area': area,
            'page': page
        }
        response = self.__session.get(self.BASE_URL, params=params)
        if response.status_code == 200:
            vacancies = response.json().get('items', [])
            print(vacancies)
            self.__vacancies.extend(vacancies)

        for v in self.__vacancies:
            if v["name"]:
                name = v["name"]
            else:
                name = "Название не указано"
            if v["alternate_url"]:
                url = v["alternate_url"]
            else:
                url = "Ссылка отсутствует"
            if v["salary"] is None or v["salary"]["from"] is None:
                salary = 0
            else:
                salary = v["salary"]["from"]
            if v["snippet"] is None or v["snippet"]["responsibility"] is None:
                description = "Описание отсутствует"
            else:
                description = v["snippet"]["responsibility"]

            self.__vacancies_new.append(
                Vacancies(name=name, url=url, description=description, salary=salary)
            )
            return self.__vacancies_new

        else:
            print("Ошибка при получении вакансий:", response.status_code)
            response.raise_for_status()




if __name__ == "__main__":
    hh_api = HHJobAPI()
    hh_api.connect()  # Проверка подключения

    # Запрос вакансий
    vacancies_new = hh_api.get_vacancies("Python")  # Поиск по всей России
    for v in vacancies_new:
        print(v)

