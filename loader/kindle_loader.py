from http.cookies import SimpleCookie

import requests

from html_parser import parse_kindle_text_to_list

from .base_loader import BaseLoader
from .config import KINDLE_CN_HISTORY_URL, KINDLE_HEADER, KINDLE_HISTORY_URL


class KindleLoader(BaseLoader):
    def __init__(self, from_year, to_year, **kwargs):
        super().__init__()
        assert to_year >= from_year
        self.from_year = from_year
        self.to_year = to_year
        self.kindle_cookie = kwargs.get("kindle_cookie", "")
        self.session = requests.Session()
        self.header = KINDLE_HEADER
        self.is_cn = kwargs.get("is_cn", False)
        self.KINDLE_URL = KINDLE_CN_HISTORY_URL if self.is_cn else KINDLE_HISTORY_URL
        self._make_years_list()

    def _parse_kindle_cookie(self):
        cookie = SimpleCookie()
        cookie.load(self.kindle_cookie)
        cookies_dict = {}
        cookiejar = None
        for key, morsel in cookie.items():
            cookies_dict[key] = morsel.value
            cookiejar = requests.utils.cookiejar_from_dict(
                cookies_dict, cookiejar=None, overwrite=True
            )
        return cookiejar

    def get_api_data(self):
        r = self.session.get(self.KINDLE_URL, headers=self.header)
        if not r.ok:
            raise Exception("Can not get kindle calendar data, please check cookie")
        data_list = parse_kindle_text_to_list(r.text)
        return data_list

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            self.number_by_date_dict[d] = 1
            self.number_list.append(1)

    def get_all_track_data(self):
        self.session.cookies = self._parse_kindle_cookie()
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
