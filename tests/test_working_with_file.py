import json
import unittest
from unittest.mock import patch, mock_open
from src.working_with_file.working_with_file_hh import JsonVacancyRepository


class TestJsonVacancyRepository(unittest.TestCase):

    def setUp(self):
        self.file_path = 'test_vacancies.json'
        self.repository = JsonVacancyRepository(self.file_path)

    @patch('builtins.open', new_callable=mock_open, read_data='[{"title": "Developer", "salary": 100000}]')
    def test_load_data_success(self, mock_file):
        vacancies = self.repository._load_data()
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]['title'], 'Developer')
        mock_file.assert_called_once_with(self.file_path, 'r', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    def test_load_data_file_not_found(self, mock_file):
        mock_file.side_effect = FileNotFoundError
        vacancies = self.repository._load_data()
        self.assertEqual(vacancies, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_load_data_json_decode_error(self, mock_file):
        mock_file.return_value.read.side_effect = json.JSONDecodeError('A JSON error occurred', 'doc', 0)
        vacancies = self.repository._load_data()
        self.assertEqual(vacancies, [])


if __name__ == '__main__':
    unittest.main()
