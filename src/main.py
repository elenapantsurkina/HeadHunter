from src.utils import top_vacancies, filter_keyword, filter_salary, display_vacancies

from src.api.api_hh import HHJobAPI


def user_interaction() -> None:
    hh_api = HHJobAPI()
    hh_api.connect()

    print("Добро пожаловать в систему поиска вакансий!")
    while True:
        query = input("Введите поисковый запрос (или 'exit' для выхода): ")
        if query.lower() == 'exit':
            break

        top_n = input("Введите количество вакансий для вывода в топ N (0 для пропуска): ")
        top_n = int(top_n) if top_n.isdigit() else None

        keyword = input("Введите ключевое слово для поиска в описании (или пропустите, нажав Enter): ").split()

        salary = input("Введите нижний порог зарплаты: ")

        vacancies = hh_api.get_vacancies(query)
        print(vacancies)

        vacancies_keyword = filter_keyword(vacancies, keyword)
        print(vacancies_keyword)

        vacancies_salary = filter_salary(vacancies_keyword, salary)
        print(vacancies_salary)

        vacancies_top = top_vacancies(vacancies_salary, top_n)
        print(vacancies_top)

        result = display_vacancies(vacancies_top)

        return result


if __name__ == '__main__':
    user_interaction()
