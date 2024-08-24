import os

current_dir = os.path.dirname(__file__)

PATH_TO_FILE = os.path.join(current_dir, '..', '..', 'HeadHunter', 'data', 'vacancies.json')
normalized_path = os.path.normpath(PATH_TO_FILE)
print(normalized_path)