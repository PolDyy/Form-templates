from file_processing_base import XLSXFileProcessingBase
from data_classes import FederalProjectsDelayed
from database.db import get_fed_prj_id_by_name, get_fed_org_id_by_name, insert_fed_prj_del

from datetime import datetime


class XLSXFileProcessing(XLSXFileProcessingBase):
    def process_data(self):

        current_year = str(datetime.now().year)
        start_row_index = 4
        years_ds_columns = self._get_years_ds_columns()
        for year in years_ds_columns:
            for index in self.df.index:

                if index < start_row_index:
                    continue

                row_date = self.df.at[index, 2]

                if (not isinstance(row_date, datetime) or
                        row_date.date() != self.COMMON_FEDERAL_PRJ_DEL['relevance_dttm'].date()):
                    continue

                proj_name = self.df.at[index, 1]
                project_date = row_date
                year_no = int(self.df.at[1, year].split(" ")[0])
                year_plan = self.current_year_ds.at[index, 3]
                year_achieved_cnt = self.current_year_ds.at[index, 4]
                year_achieved_percent = self.current_year_ds.at[index, 5]

                if current_year in self.df.at[1, year]:
                    year_left_cnt = self.current_year_ds.at[index, 6]
                    year_left_percent = self.current_year_ds.at[index, 7]
                    year_delayed_cnt = self.current_year_ds.at[index, 8]
                    year_delayed_percent = self.current_year_ds.at[index, 9]
                else:
                    year_left_cnt = None
                    year_left_percent = None
                    year_delayed_cnt = self.current_year_ds.at[index, 8]
                    year_delayed_percent = self.current_year_ds.at[index, 9]

                total_delayed_cnt = self.total_ds.at[index, 20]
                total_delayed_percent = self.total_ds.at[index, 21]

                federal_prj_id = self._get_fed_prj_id(index, proj_name)

                federal_org_id = self._get_fed_org_id(index, proj_name)

                data_record = FederalProjectsDelayed(
                    federal_prj_id=federal_prj_id,
                    federal_org_id=federal_org_id,
                    prj_date=project_date,
                    year_no=year_no,
                    year_plan=year_plan,
                    year_achieved_cnt=year_achieved_cnt,
                    year_achieved_percent=year_achieved_percent,
                    year_left_cnt=year_left_cnt,
                    year_left_percent=year_left_percent,
                    year_delayed_cnt=year_delayed_cnt,
                    year_delayed_percent=year_delayed_percent,
                    total_delayed_cnt=total_delayed_cnt,
                    total_delayed_percent=total_delayed_percent,
                    created_from=self.COMMON_FEDERAL_PRJ_DEL['created_from'],
                    created_to=self.COMMON_FEDERAL_PRJ_DEL['created_to'],
                    relevance_dttm=self.COMMON_FEDERAL_PRJ_DEL['relevance_dttm']
                )
                self.FEDERAL_PRJ_DEL.append(data_record)

        self._insert_fed_prj_del()

    def _get_years_ds_columns(self):
        columns = [3]
        columns.extend(list(range(10, 6 + 5 * self.num_last_years_ds, 5)))
        return columns

    def _get_fed_prj_id(self, index, name):
        parts = str(self.df.at[index, 0]).split('.')
        if len(parts) == 2:
            return self._id_by_name_prj(name)
        elif isinstance(parts[0], str) and parts[0].lower() == 'итого':
            return self._id_by_name_prj(parts[0].lower())
        return self._get_fed_prj_id(index - 1, self.df.at[index-1, 1])

    def _get_fed_org_id(self, index, name):
        if isinstance(name, str) and name.lower() == 'итого':
            return
        parts = str(self.df.at[index, 0]).split('.')
        if len(parts) == 3:
            return self._id_by_name_org(name)
        else:
            return

    @staticmethod
    def _id_by_name_org(name):
        org_id = get_fed_org_id_by_name(name)
        return int(org_id)

    @staticmethod
    def _id_by_name_prj(name):
        prj_id = get_fed_prj_id_by_name(name)
        return int(prj_id)

    def _insert_fed_prj_del(self):
        insert_fed_prj_del(self.FEDERAL_PRJ_DEL)
