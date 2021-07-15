#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import requests

from github_poster.loader.base_loader import BaseLoader
from github_poster.loader.config import DOTA2_CALENDAR_API


class Dota2Loader(BaseLoader):
    track_color = "#567433"
    unit = "games"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.dota2_id = kwargs.get("dota2_id", "")

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--dota2_id",
            dest="dota2_id",
            type=str,
            required=True,
            help="Check your dota2-id in-game or on the website(steamid32): "
            "https://steamid.xyz/",
        )

    def get_api_data(self):
        r = requests.get(
            DOTA2_CALENDAR_API.format(
                dota2_id=self.dota2_id,
            )
        )
        if not r.ok:
            print(f"get data2 calendar api failed {str(r.text)}")
            return []
        return r.json()

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            date = datetime.utcfromtimestamp(d["start_time"]).strftime("%Y-%m-%d")
            self.number_by_date_dict[date] += 1
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
