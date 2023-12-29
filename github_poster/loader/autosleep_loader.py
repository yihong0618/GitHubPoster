import csv
from collections import defaultdict

from datetime import datetime
from github_poster.loader.base_loader import BaseLoader


class AutoSleepLoader(BaseLoader):
    unit = "hours"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.number_by_date_dict = defaultdict(int)
        self.autosleep_file = kwargs.get("autosleep_file")

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--autosleep_file",
            dest="autosleep_file",
            type=str,
            default="autosleep.csv",
            help="autosleep json file path",
        )

    def _parse_autosleep_data(self):
        base_file = self.autosleep_file
        data_obj = {}
        with open(base_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            # eg.
            # if rows: [{"ISO8601": "2023-01-01T20:59:59+08:00", "睡眠时间": "7:31:00", "效率": "91.4" }, {"ISO8601": "2023-01-02T20:59:59+08:00", "睡眠时间": "6:31:00", "效率": "80" }]
            # result data_obj: { "2023-01-01": 91.4, "2023-01-02": 80 }
            for row in rows:
                asleep_key = "睡眠时间" if "睡眠时间" in row else "asleep"
                time_obj = datetime.strptime(row[asleep_key], "%H:%M:%S")
                hours = time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600
                date = row["ISO8601"].split("T")[0]
                data_obj[date] = round(hours, 1)
        return data_obj

    def get_api_data(self):
        return self._parse_autosleep_data()

    def make_track_dict(self):
        tracks = self.get_api_data()
        self.number_by_date_dict = tracks
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)
        return tracks

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
