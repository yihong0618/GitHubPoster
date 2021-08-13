import time

import requests

from github_poster.loader.base_loader import BaseLoader
from github_poster.loader.config import WAKATIME_SUMMARY_URL


class WakaTimeLoader(BaseLoader):
    track_color = "#9BE9A8"
    unit = "mins"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.wakatime_key = kwargs.get("wakatime_key", "")

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--wakatime_key",
            dest="wakatime_key",
            type=str,
            required=True,
            help="your wakatime api key here, "
            "more info: https://wakatime.com/settings/api-key",
        )

    def get_api_data(self):
        for year in range(self.from_year, self.to_year + 1):
            r = requests.get(
                WAKATIME_SUMMARY_URL.format(
                    wakatime_key=self.wakatime_key,
                    from_year="{}-01-01".format(year),
                    to_year="{}-12-31".format(year),
                )
            )
            if not r.ok:
                yield []
            data = r.json()
            yield from data["data"]
            # spider rule
            time.sleep(1)

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            if d:
                date = d["range"]["date"]
                self.number_by_date_dict[date] += int(
                    d["grand_total"]["total_seconds"] / 60.0
                )
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
