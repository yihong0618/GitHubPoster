import time

import pendulum
import requests

from github_poster.loader.base_loader import BaseLoader
from github_poster.loader.config import (
    LEETCODE_CN_SUBMISSIONS_URL,
    LEETCODE_SUBMISSIONS_URL,
)


class LeetcodeLoader(BaseLoader):
    unit = "subs"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.leetcode_cookie = kwargs.get("leetcode_cookie", "")
        self.is_cn = kwargs.get("cn", False)
        self.LEETCODE_URL = (
            LEETCODE_CN_SUBMISSIONS_URL if self.is_cn else LEETCODE_SUBMISSIONS_URL
        )

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--leetcode_cookie",
            dest="leetcode_cookie",
            type=str,
            required=True,
            help="",
        )
        parser.add_argument(
            "--cn",
            dest="cn",
            action="store_true",
            help="if accout is CN",
        )

    def get_api_data(self):
        offset = 0
        last_key = ""
        # leetcode may cause the permission error, just retry
        error_times = 0
        while 1:
            try:
                r = requests.get(
                    self.LEETCODE_URL.format(offset=offset, last_key=last_key),
                    cookies={"cookie": self.leetcode_cookie},
                )
                if not r.ok:
                    print(r.text)
                    break
                data = r.json()
                submissions = data["submissions_dump"]
                last_submission_this_api = submissions[-1]
                last_year = pendulum.from_timestamp(
                    last_submission_this_api["timestamp"]
                ).year
                if not submissions or last_year < self.from_year:
                    break
                yield from submissions
                if not data["has_next"]:
                    break
                last_key = data["last_key"]
                offset += 20
                time.sleep(2)
            except Exception:
                error_times += 1
                print(f"error times {error_times}")
                if error_times > 3:
                    break

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            if d:
                date = pendulum.from_timestamp(d["timestamp"]).to_date_string()
                self.number_by_date_dict[date] += 1
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
