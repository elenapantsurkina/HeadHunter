from src.utils import top_vacancies, filter_keyword, filter_salary, display_vacancies

from src.api.api_hh import HHJobAPI


def user_interaction():
    platforms = ["HHJobAPI"]
    print("Добро пожаловать в систему поиска вакансий!")
    while True:
        query = input("Введите поисковый запрос (или 'exit' для выхода): ")
        if query.lower() == 'exit':
            break

        top_n = input("Введите количество вакансий для вывода в топ N (0 для пропуска): ")
        top_n = int(top_n) if top_n.isdigit() else None

        keyword = input("Введите ключевое слово для поиска в описании (или пропустите, нажав Enter): ")

        salary = input("Введите диапазон зарплат: ")

        vacancies = platforms.get_vacancies(keyword)

        vacancies_keyword = filter_keyword(vacancies, keyword)

        vacancies_salary = filter_salary(vacancies_keyword, salary)

        vacancies_top = top_vacancies(vacancies_salary, top_n)

        result = display_vacancies(vacancies_top)

        return result


if __name__ == '__main__':
    user_interaction()
