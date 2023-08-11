import time
import requests
import json
import os
from collections import defaultdict
from datetime import datetime, timedelta

from github_poster.loader.base_loader import BaseLoader, LoadError
from github_poster.loader.config import WAKATIME_SUMMARY_URL

class WakaTimeLoader(BaseLoader):
    track_color = "#9BE9A8"
    unit = "mins"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.wakatime_key = kwargs.get("wakatime_key", "")
        self.wakatime_file = kwargs.get("wakatime_history_file", os.path.join("IN_FOLDER", "wakatime-history.json"))
        self._parse_wakatime_history()

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--wakatime_key",
            dest="wakatime_key",
            type=str,
            required=optional,
            help="your wakatime api key here, more info: https://wakatime.com/settings/api-key",
        )
        parser.add_argument(
            "--wakatime_history_file",
            dest="wakatime_history_file",
            type=str,
            default=os.path.join("IN_FOLDER", "wakatime-history.json"),
            help="Wakatime history file path",
        )

    def _parse_wakatime_history(self):
        if os.path.exists(self.wakatime_file):
            with open(self.wakatime_file, "r") as f:
                self.number_by_date_dict = json.load(f)

    def _writeback_wakatime_history(self):
        with open(self.wakatime_file, "w") as f:
            json.dump(self.number_by_date_dict, f, sort_keys=True)

    def get_api_data(self):
        if self.from_year != self.to_year:
            start_date = f"{self.from_year}-01-01"
            end_date = f"{self.to_year}-12-31"
        else:
            start_date = (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        r = requests.get(
            WAKATIME_SUMMARY_URL.format(
                wakatime_key=self.wakatime_key,
                from_year=start_date,
                to_year=end_date,
            )
        )
        if not r.ok:
            return []
        data = r.json()
        # spider rule
        time.sleep(1)
        return data.get("data", [])

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            if d:
                date = d["range"]["date"]
                if date not in self.number_by_date_dict:
                    self.number_by_date_dict[date] = int(d["grand_total"]["total_seconds"] / 60.0)
        self._writeback_wakatime_history()
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list