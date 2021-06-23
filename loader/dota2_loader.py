#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import requests

from .base_loader import BaseLoader
from .config import DOTA2_CALENDAR_API


class Dota2Loader(BaseLoader):
    def __init__(self, from_year, to_year, **kwargs):
        super().__init__()
        assert to_year >= from_year
        self.from_year = from_year
        self.to_year = to_year
        self.dota2_id = kwargs.get("dota2_id", "")
        self._make_years_list()

    def get_api_data(self):
        data_list = []
        for year in range(self.from_year, self.to_year + 1):
            r = requests.get(
                DOTA2_CALENDAR_API.format(
                    dota2_id=self.dota2_id,
                    from_year="{}-01-01".format(year),
                    to_year="{}-12-31".format(year),
                )
            )
            if not r.ok:
                print(f"get data2 calendar api failed {str(r.text)}")
        return r.json()

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            if d:
                date = datetime.utcfromtimestamp(d["start_time"]).strftime("%Y-%m-%d")
                self.number_by_date_dict[date] += 1
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
