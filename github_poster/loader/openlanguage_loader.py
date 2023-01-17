import re

import requests

from github_poster.loader.base_loader import BaseLoader, LoadError
from github_poster.loader.config import (
    OPEN_LANGUAGE_ACCOUNT_PASSWORD_DICT,
    OPEN_LANGUAGE_LOGIN_URL,
    OPEN_LANGUAGE_RECORD_URL,
    OPEN_LANGUAGE_X_ARGUS,
    OPEN_LANGUAGE_X_LADON,
)


class OpenLanguageLoader(BaseLoader):
    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.user_name = kwargs.get("openlanguage_user_name", "")
        self.password = kwargs.get("openlanguage_password", "")
        self.s = requests.Session()
        self.headers = None

    @staticmethod
    def _is_alphanumeric(a):
        return bool(re.match("^[a-zA-Z0-9]+$", a))

    def convert_string(self, a):
        convert_string = ""
        for i in a:
            convert_string = convert_string + OPEN_LANGUAGE_ACCOUNT_PASSWORD_DICT.get(i)
        return convert_string

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--openlanguage_user_name",
            dest="openlanguage_user_name",
            type=str,
            required=optional,
            help="The username of OpenLanguage",
        )
        parser.add_argument(
            "--openlanguage_password",
            dest="openlanguage_password",
            type=str,
            required=optional,
            help="The password of OpenLanguage",
        )

    def login(self):
        is_alphanumeric = self._is_alphanumeric(self.password)
        if not is_alphanumeric:
            raise LoadError(f"The password can only contain letters and numbers")
        login_headers = {
            "x-argus": OPEN_LANGUAGE_X_ARGUS,
            "x-ladon": OPEN_LANGUAGE_X_LADON,
            "sdk-version": "2",
        }

        data = {
            "mobile": self.convert_string(self.user_name),
            "password": self.convert_string(self.password),
        }
        r = self.s.post(OPEN_LANGUAGE_LOGIN_URL, headers=login_headers, data=data)
        if not r.ok:
            raise LoadError(f"Something is wrong to login -- {r.text}")
        self.headers = {
            "Content-Type": "application/json",
            "sdk-version": "2",
            "x-Tt-token": r.headers["x-Tt-Token"],
        }

    def get_api_data(self):
        month_list = self.make_month_list()
        data_list = []
        for m in month_list:
            r = self.s.get(
                OPEN_LANGUAGE_RECORD_URL.format(
                    start_date=m.to_date_string(),
                    end_date=m.end_of("month").to_date_string(),
                ),
                headers=self.headers,
            )
            if not r.ok:
                print(f"get openlanguage calendar api failed {str(r.text)}")
            try:
                data_list.extend(r.json()["records"])
            except Exception:
                pass
        return data_list

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            if d:
                number = int(d["duration"] / 60)
                if number:
                    self.number_by_date_dict[d["stat_date"]] = number
                    self.number_list.append(number)

    def get_all_track_data(self):
        self.login()
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
