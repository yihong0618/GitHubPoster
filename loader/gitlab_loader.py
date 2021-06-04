import time
from parser import GitLabParser

import requests
from pendulum import parse, period
from .base_loader import BaseLoader
from .config import GITLAB_LATEST_URL, GITLAB_ONE_DAY_URL


class GitLabLoader(BaseLoader):
    def __init__(self, from_year, to_year, **kwargs) -> None:
        super().__init__()
        assert to_year >= from_year
        self.from_year = from_year
        self.to_year = to_year
        self.user_name = kwargs.get("gitlab_user_name", "")
        self._make_years_list()
        self.left_dates = []

    def _make_left_dates(self, last_date):
        dates = list(period(parse(f"{self.from_year}-01-01"), parse(last_date)))
        self.left_dates = [i.to_date_string() for i in dates]

    def make_latest_date_dict(self):
        try:
            r = requests.get(GITLAB_LATEST_URL.format(user_name=self.user_name))
            date_dict = r.json()
            min_date = min(date_dict.keys())
            self.number_by_date_dict = date_dict
            if self.from_year > int(min_date[:4]):
                return
            self._make_left_dates(min_date)
        except Exception as e:
            raise Exception(f"Can not get gitlab data error: {str(e)}")

    def make_left_data_dict(self):
        p = GitLabParser()
        for d in self.left_dates:
            try:
                r = requests.get(
                    GITLAB_ONE_DAY_URL.format(user_name=self.user_name, date_str=d)
                )
                # spider rule
                time.sleep(0.1)
                p.feed(r.text)
                self.number_by_date_dict[d] = len(p.lis)
            except:
                # what fucking things happened just pass
                pass

    def make_track_dict(self):
        self.make_latest_date_dict()
        self.make_left_data_dict()
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
