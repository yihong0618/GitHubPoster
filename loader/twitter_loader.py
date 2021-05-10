import time
import subprocess
import sys

import pendulum
import requests

from .base_loader import BaseLoader

try:
    import twint
except ImportError:
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--user",
            "--upgrade",
            "git+https://github.com/twintproject/twint.git@origin/master#egg=twint",
        ]
    )
    import twint


class TwitterLoader(BaseLoader):
    def __init__(self, from_year, to_year, **kwargs):
        super().__init__()
        self.from_year = from_year
        self.to_year = to_year
        self.user_name = kwargs.get("twitter_user_name", "")
        self.c = twint.Config()

    def get_api_data(self):
        self.c.Username = self.user_name
        self.c.Custom["tweet"] = ["id"]
        self.c.Custom["user"] = ["bio"]
        self.c.Store_object = True
        self.c.Since = f"{self.from_year}-01-01"
        self.c.Until = f"{self.to_year}-12-31"
        twint.run.Search(self.c)
        return twint.output.tweets_list

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            date_str = d.datetime[:10]
            self.number_by_date_dict[date_str] += 1
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self._make_years_list()
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
