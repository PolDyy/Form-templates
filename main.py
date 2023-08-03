import os
from database.db import create_tables
from custom_exception import EmptyDirException
from forms_validator import XLSXValidator
from file_processing import XLSXFileProcessing


output_data_list = []


def start():
    create_tables()
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    forms_dir = os.path.join(current_dir, 'forms')

    xlsx_files = []
    for file_name in os.listdir(forms_dir):
        if file_name.endswith('.xlsx'):
            xlsx_files.append(os.path.join(forms_dir, file_name))

    if not xlsx_files:
        raise EmptyDirException("Файлов не обнаруженно")

    for file_path in xlsx_files:

        dates = XLSXValidator.validator(file_path)

        if not dates:
            continue

        file_processing = XLSXFileProcessing(file_path, dates)
        file_processing.process_data()
        file_processing.to_file()


start()
