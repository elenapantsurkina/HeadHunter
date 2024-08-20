import requests


def search_vacancies(query, top_n=None, keyword=None):
    """
    Запрашивает вакансии с hh.ru по заданному запросу.

    :param query: строка запроса для поиска вакансий
    :param top_n: количество топовых вакансий по зарплате
    :param keyword: ключевое слово для поиска в описании
    :return: список вакансий
    """
    url = f'https://api.hh.ru/vacancies'
    params = {
        'text': query,
        'order_by': 'salary',  # сортируем по зарплате
        'per_page': 50,  # количество вакансий на странице
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f'Ошибка при обращении к API: {response.status_code}')
        return []

    vacancies = response.json().get('items', [])

    if top_n is not None:
        vacancies = sorted(vacancies, key=lambda x: x['salary'] if x['salary'] else 0, reverse=True)[:top_n]

    if keyword:
        vacancies = [vacancy for vacancy in vacancies if keyword.lower() in vacancy['snippet']['requirement'].lower()]

    return vacancies


def display_vacancies(vacancies):
    """
    Отображает информацию о вакансиях.

    :param vacancies: список вакансий
    """
    if not vacancies:
        print("Вакансии не найдены.")
        return

    for idx, vacancy in enumerate(vacancies, start=1):
        print(f"{idx}. {vacancy['name']}")
        print(f"   URL: {vacancy['alternate_url']}")
        salary = vacancy['salary']
        if salary:
            print(f"   Зарплата: от {salary['from']} до {salary['to']} {salary['currency']}")
        else:
            print("   Зарплата не указана")
        print(f"   Описание: {vacancy['snippet']['requirement']}\n")


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
