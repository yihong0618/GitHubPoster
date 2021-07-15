import hashlib
import json

import requests

from github_poster.loader.base_loader import BaseLoader, LoadError
from github_poster.loader.config import (
    CICHANG_CLAENDAR_URL,
    CICHANG_COVERT_URL,
    CICHANG_LOGIN_URL,
    HJ_APPKEY,
)


class CiChangLoader(BaseLoader):
    unit = "words"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.user_name = kwargs.get("cichang_user_name", "")
        self.password = kwargs.get("cichang_password", "")
        self.s = requests.Session()

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--cichang_user_name",
            dest="cichang_user_name",
            type=str,
            required=True,
            help="The username of CiChang",
        )
        parser.add_argument(
            "--cichang_password",
            dest="cichang_password",
            type=str,
            required=True,
            help="The password of CiChang",
        )

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
            raise LoadError(f"Someting is wrong to login -- {r.text}")
        club_auth_cookie = r.json()["Data"]["Cookie"]
        data = {"club_auth_cookie": club_auth_cookie}
        headers = {"hj_appkey": HJ_APPKEY, "Content-Type": "application/json"}
        # real login to get real token
        r = self.s.post(CICHANG_COVERT_URL, headers=headers, data=json.dumps(data))
        if not r.ok:
            raise LoadError(f"Get real token failed -- {r.text}")
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
            except Exception:
                # just pass for now
                pass
        return data_list

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            if d:
                number = d["studyCount"]
                if number:
                    self.number_by_date_dict[d["studyDate"].replace("/", "-")] = number
                    self.number_list.append(number)

    def get_all_track_data(self):
        self.login()
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
