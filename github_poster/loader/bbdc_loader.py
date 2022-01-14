import json
import os.path
from datetime import datetime

import requests

from github_poster.loader.base_loader import BaseLoader, LoadError
from github_poster.loader.config import BBDC_API_URL


class BBDCLoader(BaseLoader):
    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.user_id = kwargs.get("bbdc_user_id", "")

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--bbdc_user_id",
            dest="bbdc_user_id",
            type=str,
            required=optional,
            help="BBDC user id",
        )

    def update_cache(self):
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
        cache = None
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        if not os.path.exists(cache_path):
            if not self.user_id:
                raise LoadError("user id is required")
            cache = {'id': self.user_id, 'data': {}}
        else:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                self.user_id = cache.get("id", "")
                if not self.user_id:
                    raise LoadError("user_id not found in cache.")

        year = datetime.now().year

        resp = requests.get(BBDC_API_URL.format(user_id=self.user_id))
        if not resp.ok:
            raise LoadError(
                "Meet unexpected error."
            )
        body = resp.json()['data_body']
        duration = body['durationList']
        learn = body['durationList']

        for i in duration:
            full_date = self.today_transform(i['date'])
            if not full_date in cache['data']:
                cache['data'][full_date] = {}

            dur = i['duration']
            cache['data'][full_date]['time'] = dur

        for i in learn:
            full_date = self.today_transform(i['date'])
            if not full_date in cache['data']:
                cache['data'][full_date] = {}

            learn = i['learnNum']
            review = i['reviewNum']
            cache['data'][full_date]['learn'] = learn
            cache['data'][full_date]['review'] = review

    @staticmethod
    def today_transform(date):
        if not date == "今日":
            return f"{datetime.today().year}-{date}"
        else:
            return datetime.today().strftime("%Y-%m-%d")

    def get_api_data(self):
        pass

    def make_track_dict(self):
        pass

    def get_all_track_data(self):
        pass
