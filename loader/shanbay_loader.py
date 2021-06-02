import requests
from .base_loader import BaseLoader
from .config import SHANBAY_CALENDAR_API


class ShanBayLoader(BaseLoader):
    def __init__(self, from_year, to_year, **kwargs) -> None:
        super().__init__()
        assert to_year >= from_year
        self.from_year = from_year
        self.to_year = to_year
        self.user_name = kwargs.get("shanbay_user_name", "")
        self._make_years_list()

    def get_api_data(self):
        month_list = self.make_month_list()
        data_list = []
        for m in month_list:
            r = requests.get(
                SHANBAY_CALENDAR_API.format(
                    user_name=self.user_name,
                    start_date=m.to_date_string(),
                    end_date=m.end_of("month").to_date_string(),
                )
            )
            if not r.ok:
                print(f"get shanbay calendar api failed {str(r.text)}")
            try:
                data_list.extend(r.json()["logs"])
            except:
                # just pass for now
                pass
        return data_list

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            if d:
                self.number_by_date_dict[d["date"]] = 1
                self.number_list.append(1)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
