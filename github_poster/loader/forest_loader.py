import json

import pendulum
import requests

from github_poster.loader.base_loader import BaseLoader, LoadError
from github_poster.loader.config import FOREST_CLAENDAR_URL, FOREST_LOGIN_URL


class ForestLoader(BaseLoader):
    unit = "trees"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.user_email = kwargs.get("forest_email", "")
        self.password = kwargs.get("forest_password", "")
        self.user_id = None
        self.s = requests.Session()

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--forest_email",
            dest="forest_email",
            type=str,
            required=optional,
            help="The email of forest",
        )
        parser.add_argument(
            "--forest_password",
            dest="forest_password",
            type=str,
            required=optional,
            help="The password of Forest",
        )

    def login(self):
        data = {"session": {"email": self.user_email, "password": self.password}}
        headers = {"Content-Type": "application/json"}
        r = self.s.post(FOREST_LOGIN_URL, headers=headers, data=json.dumps(data))
        if not r.ok:
            raise LoadError(f"Someting is wrong to login -- {r.text}")
        self.user_id = r.json()["user_id"]

    def get_api_data(self):
        date = str(self.from_year) + "-01-01"
        r = self.s.get(FOREST_CLAENDAR_URL.format(date=date, user_id=self.user_id))
        if not r.ok:
            raise LoadError(f"Someting is wrong to get data-- {r.text}")
        return r.json()["plants"]

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            date = pendulum.parse(d["created_at"], tz=self.time_zone).to_date_string()
            self.number_by_date_dict[date] += d["tree_count"]
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.login()
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
