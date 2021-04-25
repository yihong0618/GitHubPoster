import time
import hashlib
import json

import pendulum
import requests

from .base_loader import BaseLoader
from .config import (
    TIME_ZONE,
    HJ_APPKEY,
    CICHANG_LOGIN_URL,
    CICHANG_COVERT_URL,
    CICHANG_CLAENDAR_URL,
)


class CiChangLoader(BaseLoader):
    def __init__(self, from_year, to_year, **kwargs):
        super().__init__()
        self.from_year = from_year
        self.to_year = to_year
        self.user_name = kwargs.get("cichang_user_name", "")
        self.password = kwargs.get("cichang_password", "")
        self.s = requests.Session()

    @staticmethod
    def _md5_encode(string):
        m = hashlib.md5()
        m.update(string.encode())
        return m.hexdigest()

    def login(self):
        password_md5 = self._md5_encode(self.password)
        r = self.s.get(
            CICHANG_LOGIN_URL.format(user_name=self.user_name, password=password_md5)
        )
        if not r.ok:
            raise Exception(f"Someting is wrong to login -- {r.text}")
        club_auth_cookie = r.json()["Data"]["Cookie"]
        data = {"club_auth_cookie": club_auth_cookie}
        headers = {"hj_appkey": HJ_APPKEY, "Content-Type": "application/json"}
        # real login to get real token
        r = self.s.post(CICHANG_COVERT_URL, headers=headers, data=json.dumps(data))
        if not r.ok:
            raise Exception(f"Get real token failed -- {r.text}")
        data = r.json()["data"]
        access_token = data["access_token"]
        user_id = data["user_id"]
        headers["Access-Token"] = access_token
        self.s.headers = headers
        self.user_id = user_id

    def get_api_data(self):
        month_list = self.make_month_list()
        data_list = []
        for m in month_list:
            print(m.to_date_string(), m.end_of("month").to_date_string(), self.user_id)
            r = self.s.get(
                CICHANG_CLAENDAR_URL.format(
                    user_id=self.user_id,
                    start_date=m.to_date_string(),
                    end_date=m.end_of("month").to_date_string(),
                )
            )
            if not r.ok:
                print(f"get cichang calendar api failed {str(r.text)}")
            try:
                data_list.extend(r.json()["data"]["studyCountDays"])
            except:
                # just pass for now
                pass
        return data_list

    def make_special_number(self):
        """
        This func is to make special color number for poster
        special_number1 top 10%
        special_number2  top 10 % - 25%
        """
        # before python below 3.5 maybe need to sort
        number_list_set = sorted(list(set(self.number_list)))
        number_list_set_len = len(number_list_set)
        if number_list_set_len < 5:
            return
        elif len(self.number_list) < 10:
            self.sepecial_number1 = number_list_set[-1]
            self.sepecial_number2 = number_list_set[-2]
        else:
            self.sepecial_number1 = number_list_set[-1 * int(number_list_set_len * 0.1)]
            self.sepecial_number2 = number_list_set[
                -1 * int(number_list_set_len * 0.25)
            ]

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            if d:
                number = d["studyCount"]
                self.number_by_date_dict[d["studyDate"].replace("/", "-")] = number
                self.number_list.append(number)

    def get_all_track_data(self):
        self._make_years_list()
        self.login()
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
