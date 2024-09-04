from src.vacancies import Vacancies
def top_vacancies(vacancies_salary, top_n):
    """Функция выводящая топ вакансий"""
    vacancies_top = sorted(vacancies_salary, key=lambda x: x.salary, reverse=True)[:top_n]
    return vacancies_top


def filter_keyword(vacancies, keyword):
    if isinstance(keyword, list) and keyword:
        vacancies_keyword = [
            vacancy for vacancy in vacancies
            if all(word in vacancy.description.lower().split() for word in keyword)
        ]
        return vacancies_keyword
    return vacancies



def filter_salary(vacancies_keyword, salary):
    vacancies_salary = []
    for v in vacancies_keyword:
        if int(salary) >= v.salary:
            vacancies_salary.append(v)
    return vacancies_salary


def display_vacancies(vacancies_top):
    """Отображает информацию о вакансиях для пользователя"""
    if not vacancies_top:
        print("Вакансии не найдены.")
        return

    for idx, vacancy in enumerate(vacancies_top, start=1):
        print(f"{idx}. {vacancy.name}")
        print(f"   URL: {vacancy.url}")
        salary = vacancy.salary
        if salary:
            print(f"   Нижний порог зарплаты : {salary}")
        else:
            print("   Зарплата не указана")
        print(f"   Описание: {vacancy.description}\n")
