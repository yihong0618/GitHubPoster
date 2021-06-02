import pendulum
import requests

from .base_loader import BaseLoader
from .config import DUOLINGO_CALENDAR_API


class DuolingoLoader(BaseLoader):
    def __init__(self, from_year, to_year, **kwargs):
        super().__init__()
        self.from_year = from_year
        self.to_year = to_year
        self.user_name = kwargs.get("duolingo_user_name", "")
        self._make_years_list()

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
            except:
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
