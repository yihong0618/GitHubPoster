#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from github_poster.loader.base_loader import BaseLoader
from github_poster.loader.config import COVID_API


class CovidLoader(BaseLoader):
    unit = ""

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.covid_area = kwargs.get("covid_area", "")

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--covid_area",
            dest="covid_area",
            type=str,
            default="China",
            help="https://pomber.github.io/covid19/timeseries.json",
        )

    def get_api_data(self):
        r = requests.get(COVID_API)
        if not r.ok:
            print(f"get covid api failed {str(r.text)}")
            return []
        return r.json()

    @staticmethod
    def __format_date(date):
        date_string_list = date.split("-")
        if len(date_string_list[1]) == 1:
            date_string_list[1] = "0" + date_string_list[1]
        if len(date_string_list[2]) == 1:
            date_string_list[2] = "0" + date_string_list[2]
        return "-".join(date_string_list)

    def make_track_dict(self):
        all_data_dict = self.get_api_data()
        print(list(all_data_dict.keys()))
        area_data_list = all_data_dict.get(self.covid_area)
        date_list = [self.__format_date(i.get("date")) for i in area_data_list]
        a = [i.get("confirmed") for i in area_data_list]
        value_increase_list = [a[0]] + [a[i] - a[i - 1] for i in range(1, len(a))]
        for date, num in zip(date_list, value_increase_list):
            self.number_by_date_dict[date] = num
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
