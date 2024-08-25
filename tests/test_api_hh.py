import unittest
from unittest.mock import patch, Mock
import requests
from src.api.api_hh import HHJobAPI
from src.vacancies import Vacancies


class TestHHJobAPI(unittest.TestCase):
    @patch.object(requests.Session, 'get')
    def test_connect_success(self, mock_get):
        # Настраиваем мок, чтобы он возвращал успешный ответ
        mock_get.return_value = Mock(status_code=200)

        api = HHJobAPI()
        # Используем метод connect, который проверяет подключение
        api.connect()

        # Проверяем, что метод get был вызван с правильным URL
        mock_get.assert_called_once_with(api.BASE_URL)

    @patch.object(requests.Session, 'get')
    def test_connect_failure(self, mock_get):
        # Настраиваем мок, чтобы он возвращал ответ с ошибкой
        response_mock = Mock()
        response_mock.status_code = 404
        response_mock.raise_for_status.side_effect = requests.exceptions.HTTPError('404 Not Found')

        mock_get.return_value = response_mock

        api = HHJobAPI()

        with self.assertRaises(requests.exceptions.HTTPError):
            api.connect()

        # Проверяем, что метод get был вызван с правильным URL
        mock_get.assert_called_once_with(api.BASE_URL)

    @patch.object(requests.Session, 'get')
    def test_get_vacancies_success(self, mock_get):
        # Настраиваем мок-ответ для успешного запроса
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'items': [
                {
                    'name': 'Программист',
                    'alternate_url': 'https://example.com/vacancy1',
                    'salary': {'from': 100000},
                    'snippet': {'responsibility': 'Разработка приложений'}
                },
                {
                    'name': None,
                    'alternate_url': None,
                    'salary': None,
                    'snippet': None
                }
            ]
        }
        mock_get.return_value = mock_response

        api = HHJobAPI()
        vacancies = api.get_vacancies('Программист')

        # Проверяем, что метод get был вызван с правильными параметрами
        mock_get.assert_called_once_with(api.BASE_URL, params={'text': 'Программист', 'area': None, 'page': 20})

        # Проверяем, что вакансии были получены корректно
        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0].name, 'Программист')
        self.assertEqual(vacancies[0].url, 'https://example.com/vacancy1')
        self.assertEqual(vacancies[0].salary, 100000)
        self.assertEqual(vacancies[0].description, 'Разработка приложений')

        # Проверяем вторую вакансию с отсутствующими данными
        self.assertEqual(vacancies[1].name, 'Название не указано')
        self.assertEqual(vacancies[1].url, 'Ссылка отсутствует')
        self.assertEqual(vacancies[1].salary, 0)
        self.assertEqual(vacancies[1].description, 'Описание отсутствует')

    # @patch.object(requests.Session, 'get')
    # def test_get_vacancies_failure(self, mock_get):
    #     # Настраиваем мок-ответ для ошибки
    #     mock_response = Mock()
    #     mock_response.status_code = 404
    #     mock_get.return_value = mock_response
    #
    #     api = HHJobAPI()
    #
    #     with self.assertRaises(requests.exceptions.HTTPError):
    #         api.get_vacancies('Программист')
    #
    #     # Проверяем, что метод get был вызван с правильными параметрами
    #     mock_get.assert_called_once_with(api.BASE_URL, params={'text': 'Программист', 'area': None, 'page': 20})


if __name__ == '__main__':
    unittest.main()
