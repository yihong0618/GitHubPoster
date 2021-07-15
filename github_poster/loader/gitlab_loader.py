import time

import requests
from pendulum import parse, period

from github_poster.html_parser import GitLabParser
from github_poster.loader.base_loader import BaseLoader, LoadError
from github_poster.loader.config import GITLAB_LATEST_URL, GITLAB_ONE_DAY_URL


class GitLabLoader(BaseLoader):
    track_color = "#ACD5F2"
    unit = "cons"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.user_name = kwargs.get("gitlab_user_name", "")
        self.gitlab_base_url = kwargs.get("base_url") or "https://gitlab.com"
        self.gitlab_session = kwargs.get("session")
        self.left_dates = []

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--gitlab_user_name",
            dest="gitlab_user_name",
            type=str,
            required=True,
            help="",
        )

        parser.add_argument(
            "--base_url",
            dest="base_url",
            type=str,
            default="https://gitlab.com",
            help="specify the base url of your self-managed gitlab",
        )
        parser.add_argument(
            "--session",
            dest="session",
            type=str,
            default="",
            help="use gitlab_session from Cookies "
            "if your gitlab instance needs to sign in",
        )

    def _make_left_dates(self, last_date):
        dates = list(period(parse(f"{self.from_year}-01-01"), parse(last_date)))
        self.left_dates = [i.to_date_string() for i in dates]

    def _set_cookies(self):
        if self.gitlab_session:
            return {"_gitlab_session": self.gitlab_session}

        return {}

    def make_latest_date_dict(self):
        try:
            r = requests.get(
                GITLAB_LATEST_URL.format(
                    gitlab_base_url=self.gitlab_base_url, user_name=self.user_name
                ),
                cookies=self._set_cookies(),
            )
            date_dict = r.json()
            min_date = min(date_dict.keys())
            self.number_by_date_dict = date_dict
            if self.from_year > int(min_date[:4]):
                return
            self._make_left_dates(min_date)
        except Exception as e:
            raise LoadError(f"Can not get gitlab data error: {str(e)}")

    def make_left_data_dict(self):
        p = GitLabParser()
        for d in self.left_dates:
            try:
                r = requests.get(
                    GITLAB_ONE_DAY_URL.format(
                        gitlab_base_url=self.gitlab_base_url,
                        user_name=self.user_name,
                        date_str=d,
                    ),
                    cookies=self._set_cookies(),
                )
                # spider rule
                time.sleep(0.1)
                p.feed(r.text)
                self.number_by_date_dict[d] = len(p.lis)
            except Exception:
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
