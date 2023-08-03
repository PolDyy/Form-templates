import os
import re
import pandas as pd
from pprint import pprint
from typing import Optional
from datetime import datetime, timedelta
from custom_exception import NameFileException, R1Exception


class XLSXValidator:

    @staticmethod
    def _name_validator(file_path: str) -> None:

        if "форма эталон" not in os.path.basename(file_path).lower():
            raise NameFileException("Имя файла не содержит 'форма эталон'")

    @staticmethod
    def _date_validator(file_path: str) -> tuple[datetime, datetime, datetime]:

        match = re.search(r'\((\d{2}\.\d{2}\.\d{4})\)', os.path.basename(file_path))
        if not match:
            raise NameFileException("Имя файла не содержит дату")

        date_str = match.group(1)
        file_date = datetime.strptime(date_str, '%d.%m.%Y')
        created_from = file_date - timedelta(days=file_date.weekday())
        created_to = created_from + timedelta(days=6, hours=23, minutes=59)

        return file_date, created_from, created_to

    @staticmethod
    def _r1_field_validator(file_path: str):
        df = pd.read_excel(file_path, header=None, usecols="R,S,T,U,V", skiprows=0)
        date_from_r1 = None
        for col in df.columns:
            cell_value = df.at[0, col]
            if pd.notna(cell_value):
                date_from_r1 = cell_value
                break

        if pd.notna(date_from_r1):
            pd.to_datetime(date_from_r1)
        else:
            raise R1Exception("Ячейка R1 пустая")

    @classmethod
    def validator(cls, file_path) -> Optional[tuple[datetime, datetime, datetime]]:
        try:
            cls._name_validator(file_path)
            cls._r1_field_validator(file_path)

            dates = cls._date_validator(file_path)

            return dates
        except NameFileException as ex:
            print("Ошибка валидации: ", ex.message)
            return
        except R1Exception as ex:
            print("Ошибка валидации: ", ex.message)
            return
        except ValueError:
            print("Ошибка: ячейка R1 не содержит дату")