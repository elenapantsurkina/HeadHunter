from src.utils import search_vacancies, display_vacancies
import requests
from src.api.api_hh import HHJobAPI


def user_interaction():
    print("Добро пожаловать в систему поиска вакансий!")
    while True:
        query = input("Введите поисковый запрос (или 'exit' для выхода): ")
        if query.lower() == 'exit':
            break

        top_n = input("Введите количество топ вакансий по зарплате (0 для пропуска): ")
        top_n = int(top_n) if top_n.isdigit() else None

        keyword = input("Введите ключевое слово для поиска в описании (или пропустите, нажав Enter): ")

        vacancies = search_vacancies(query, top_n if top_n > 0 else None, keyword if keyword else None)
        display_vacancies(vacancies)


if __name__ == '__main__':
    user_interaction()
