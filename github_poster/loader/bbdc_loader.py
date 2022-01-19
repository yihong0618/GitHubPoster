import json
import os.path
from datetime import datetime

import requests

from github_poster.loader.base_loader import BaseLoader, LoadError
from github_poster.loader.config import BBDC_API_URL


class BBDCLoader(BaseLoader):
    unit = "minutes"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.user_id = kwargs.get("bbdc_user_id", "")
        self.type = kwargs.get("bbdc_type", "time")

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--bbdc_user_id",
            dest="bbdc_user_id",
            type=str,
            required=optional,
            help="BBDC user id",
        )
        parser.add_argument(
            "--bbdc_type",
            dest="bbdc_type",
            type=str,
            default="time",
            choices=["time", "word"],
            help="generate count type [time,word]",
        )

    def _update_cache(self):
        """
        cache structure

        id: user-id
        data:
          2021-1-1:
            learn: 20
            time: 5
            review: 20
        """

        data_path = os.path.join(os.getcwd(), "data")
        cache_path = os.path.join(os.getcwd(), "data", "bbdc.json")

        if not os.path.exists(data_path):
            os.mkdir(data_path)
        if not os.path.exists(cache_path):
            if not self.user_id:
                raise LoadError("user id is required")
            cache = {"id": self.user_id, "data": {}}
        else:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache = json.load(f)
                self.user_id = cache.get("id", "")
                if not self.user_id:
                    raise LoadError("user_id not found in cache.")

        resp = requests.get(BBDC_API_URL.format(user_id=self.user_id))
        if not resp.ok:
            raise LoadError(f"Meet network error. {resp.reason}")
        data = resp.json()
        if data["result_code"] != 200:
            raise LoadError(f"Unexpected error. {data}")

        body = data["data_body"]
        duration = body["durationList"]
        learn = body["learnList"]

        for i in duration:
            full_date = self.today_transform(i["date"])
            if full_date not in cache["data"]:
                cache["data"][full_date] = {}

            dur = i["duration"]
            cache["data"][full_date]["time"] = dur

        for i in learn:
            full_date = self.today_transform(i["date"])
            if full_date not in cache["data"]:
                cache["data"][full_date] = {}

            learn = i["learnNum"]
            review = i["reviewNum"]
            cache["data"][full_date]["learn"] = learn
            cache["data"][full_date]["review"] = review

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False)

        return cache

    @staticmethod
    def today_transform(date):
        if not date == "今日":
            return f"{datetime.today().year}-{date}"
        else:
            return datetime.today().strftime("%Y-%m-%d")

    def make_track_dict(self):
        cache = self._update_cache()
        data = cache["data"]
        for date, value in data.items():
            year = int(date[:4])
            if year not in self.year_list:
                pass
            else:
                if self.type == "time":
                    self.number_by_date_dict[date] = value["time"]
                elif self.type == "word":
                    BBDCLoader.unit = "words"
                    self.number_by_date_dict[date] = value["learn"] + value["review"]
                else:
                    raise LoadError(f"unsupport type {self.type}")
                self.number_by_date_dict = dict(
                    sorted(self.number_by_date_dict.items())
                )
                self.number_list = list(self.number_by_date_dict.values())

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
