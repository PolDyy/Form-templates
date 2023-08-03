from datetime import datetime
import pandas as pd
from dataclasses import asdict

from data_classes import FederalProjectsDelayed, FederalProjects, FederalOrganizations, CommonFederalProjectsDelayed
from database.db import insert_fed_prjs, insert_fed_orgs


class XLSXFileProcessingBase:
    FEDERAL_PRJ: list[FederalProjects] = []
    FEDERAL_ORG: list[FederalOrganizations] = []
    FEDERAL_PRJ_DEL: list[FederalProjectsDelayed] = []

    def __init__(self, file_path: str, dates: tuple[datetime, datetime, datetime]):

        self.COMMON_FEDERAL_PRJ_DEL = self._common_federal_prj_del_init(dates)
        self.df = self._get_df(file_path)
        self._datasets_init()

    @staticmethod
    def _get_df(file_path):

        df = pd.read_excel(file_path)
        columns = list(range(len(df.columns.to_list())))
        df.columns = columns
        return df

    def _datasets_init(self):
        self.a_column_ds = self._a_column_ds_init()
        self.current_year_ds = self._current_year_ds_init()
        self.num_last_years_ds = self._num_last_years_ds_init()
        self.total_ds = self._total_ds_init()

    def _a_column_ds_init(self):

        df = self.df

        end_index = df[df.iloc[:, 0] == 'Итого'].index[0] + 1
        start_index = 4

        a_column_ds = df.iloc[start_index:end_index, 0]
        self._fed_org_fed_prj_init(start_index, end_index)
        return a_column_ds

    def _current_year_ds_init(self):
        current_year_ds = self.df.iloc[:, 3:10].dropna()
        return current_year_ds

    def _num_last_years_ds_init(self):
        df = self.df
        num_last_years_ds = 0
        for col_index, col_value in enumerate(df.iloc[1, 10:], start=10):
            if isinstance(col_value, str) and 'итого' not in col_value.lower():
                num_last_years_ds += 1

        return num_last_years_ds

    def _total_ds_init(self):
        df = self.df
        total_index = 0
        for col_index, col_value in enumerate(df.iloc[1, 10:], start=10):
            if isinstance(col_value, str) and 'итого' in col_value.lower():
                total_index = col_index
                break
        total_ds = df.iloc[4:, total_index:total_index + 2].dropna()
        return total_ds

    def _fed_org_fed_prj_init(self, start_index, end_index):
        df = self.df
        while start_index < end_index:
            data_id = df.iloc[start_index, 0]
            data_name = df.iloc[start_index, 1]

            if 'итого' in data_id.lower():

                fed_prj = FederalProjects(
                    name=data_id.lower()
                )
                self.FEDERAL_PRJ.append(fed_prj)
                break

            data_id = data_id.split('.')

            if len(data_id) == 2:
                self._set_fed_prj(data_name)
            else:
                self._set_fed_org(data_name)

            start_index += 2
        self._insert_fed_org_and_fed_prj_to_db()

    def _set_fed_org(self, data_name):
        fed_org = FederalOrganizations(
            name=data_name
        )
        self.FEDERAL_ORG.append(fed_org)

    def _set_fed_prj(self, data_name):
        fed_prj = FederalProjects(
            name=data_name
        )
        self.FEDERAL_PRJ.append(fed_prj)

    @staticmethod
    def _common_federal_prj_del_init(dates: tuple[datetime, datetime, datetime]):

        federal_prj_del = CommonFederalProjectsDelayed(
            relevance_dttm=dates[0],
            created_from=dates[1],
            created_to=dates[2]
        )
        return asdict(federal_prj_del)

    def to_file(self):
        for prj in self.FEDERAL_PRJ:
            fed_prj = prj.as_string()
            with open('results/fed_prj.txt', 'a+') as file:
                file.write('\n' + fed_prj + '\n')

        for org in self.FEDERAL_ORG:
            fed_org = org.as_string()
            with open('results/fed_org.txt', 'a+') as file:
                file.write('\n' + fed_org + '\n')

        for prj_del in self.FEDERAL_PRJ_DEL:
            fed_prj_del = prj_del.as_string()
            with open('results/fed_prj_del.txt', 'a+') as file:
                file.write('\n' + fed_prj_del + '\n')

    def _insert_fed_org_and_fed_prj_to_db(self):
        fed_org = self.FEDERAL_ORG
        fed_prj = self.FEDERAL_PRJ
        insert_fed_prjs(fed_prj)
        insert_fed_orgs(fed_org)
