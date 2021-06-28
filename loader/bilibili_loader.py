import time
from collections import defaultdict
from http.cookies import SimpleCookie

import pendulum
import requests

from .base_loader import BaseLoader, LoadError
from .config import BILIBILI_HISTORY_URL


class BilibiliLoader(BaseLoader):
    def __init__(self, from_year, to_year, **kwargs):
        super().__init__()
        self.from_year = from_year
        self.to_year = to_year
        self.number_by_date_dict = defaultdict(int)
        self.session = requests.Session()
        self.bilibili_cookie = kwargs.get("bilibili_cookie", "")
        self._make_years_list()

    def _parse_bilibili_cookie(self):
        cookie = SimpleCookie()
        cookie.load(self.bilibili_cookie)
        cookies_dict = {}
        cookiejar = None
        for key, morsel in cookie.items():
            cookies_dict[key] = morsel.value
            cookiejar = requests.utils.cookiejar_from_dict(
                cookies_dict, cookiejar=None, overwrite=True
            )
        return cookiejar

    def get_api_data(self, max_oid="", view_at="", data_list=[]):
        r = self.session.get(
            BILIBILI_HISTORY_URL.format(max_oid=max_oid, view_at=view_at)
        )
        if not r.ok:
            raise LoadError(
                "Can not get bilibili history data, please check your cookie"
            )
        data = r.json()["data"]
        if not data["list"]:
            return data_list
        lst = data["list"]
        max_oid = lst[-1]["history"]["oid"]
        view_at = lst[-1]["view_at"]
        data_list.extend(lst)
        # spider rule
        time.sleep(0.1)
        return self.get_api_data(max_oid=max_oid, view_at=view_at, data_list=data_list)

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            date_str = pendulum.from_timestamp(
                d["view_at"], tz=self.time_zone
            ).to_date_string()
            self.number_by_date_dict[date_str] += 1
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        # first we need to activate the session with cookie str from `chrome`
        self.session.cookies = self._parse_bilibili_cookie()

        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
