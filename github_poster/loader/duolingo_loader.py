import pendulum
import requests

from github_poster.loader.base_loader import BaseLoader
from github_poster.loader.config import DUOLINGO_CALENDAR_API


class DuolingoLoader(BaseLoader):
    unit = "XP"

    def __init__(self, from_year, to_year, **kwargs):
        super().__init__(from_year, to_year)
        self.user_name = kwargs.get("user_name", "")

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--user_name",
            dest="user_name",
            type=str,
            help="",
            required=True,
        )

    def get_api_data(self):
        month_list = self.make_month_list()
        data_list = []
        for m in month_list:
            r = requests.get(
                DUOLINGO_CALENDAR_API.format(
                    user_id=self.user_name,
                    start_date=m.to_date_string(),
                    end_date=m.end_of("month").to_date_string(),
                )
            )
            if not r.ok:
                print(f"get duolingo calendar api failed {str(r.text)}")
            try:
                data_list.extend(r.json()["summaries"])
            except Exception:
                # just pass for now
                pass
        return data_list

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            date_str = pendulum.from_timestamp(d["date"]).to_date_string()
            number = d["gainedXp"]
            if number:
                self.number_by_date_dict[date_str] = number
                self.number_list.append(number)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
