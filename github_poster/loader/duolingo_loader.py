import pendulum
import requests

from github_poster.loader.base_loader import BaseLoader
from github_poster.loader.config import DUOLINGO_CALENDAR_API, DUOLINGO_LOGIN_URL


class DuolingoLoader(BaseLoader):
    unit = "XP"
    track_color = "#78C800"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.user_name = kwargs.get("duolingo_user_name", "")
        self.password = kwargs.get("duolingo_password", "")
        self.session = requests.Session()
        # duolingo name to get the calendar
        self.duolingo_id = ""

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--duolingo_user_name",
            dest="duolingo_user_name",
            type=str,
            help="",
            required=optional,
        )
        parser.add_argument(
            "--duolingo_password",
            dest="duolingo_password",
            type=str,
            help="",
            required=optional,
        )

    def login(self):
        r = self.session.post(
            DUOLINGO_LOGIN_URL,
            params={"login": self.user_name, "password": self.password},
        )
        if r.status_code != 200:
            raise Exception("Login failed")
        self.duolingo_id = r.json()["user_id"]

    def get_api_data(self):
        month_list = self.make_month_list()
        for m in month_list:
            r = self.session.get(
                DUOLINGO_CALENDAR_API.format(
                    user_id=self.duolingo_id,
                    start_date=m.to_date_string(),
                    end_date=m.end_of("month").to_date_string(),
                )
            )
            if not r.ok:
                print(f"get duolingo calendar api failed {str(r.text)}")
            try:
                yield from r.json()["summaries"]
            except Exception:
                # just pass for now
                pass

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            date_str = pendulum.from_timestamp(d["date"]).to_date_string()
            number = d["gainedXp"]
            if number:
                self.number_by_date_dict[date_str] = number
                self.number_list.append(number)

    def get_all_track_data(self):
        self.login()
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
