import json
import os

from collections import defaultdict
from datetime import datetime

from github_poster.loader.base_loader import BaseLoader


def timestamp_to_date(microseconds):
    return datetime.fromtimestamp(microseconds / 1e6).strftime("%Y-%m-%d")


class GoogleKeepLoader(BaseLoader):
    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.number_by_date_dict = defaultdict(int)
        self.gkeep_dir = kwargs.get("gkeep_dir")

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--gkeep_dir",
            dest="gkeep_dir",
            type=str,
            default="Takeout/Keep",
            help="Google Keep export directory",
        )

    def get_data_from_file(self, gkeep_dir):
        for filename in os.listdir(gkeep_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(gkeep_dir, filename)

                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    created_timestamp_usec = data.get("createdTimestampUsec", 0)
                    date = timestamp_to_date(created_timestamp_usec)

                    self.number_by_date_dict[date] = (
                        self.number_by_date_dict.get(date, 0) + 1
                    )

    def get_api_data(self):
        pass

    def make_track_dict(self):
        self.get_data_from_file(self.gkeep_dir)

        for k, v in self.number_by_date_dict.items():
            self.number_list.append(v)

            year = int(k[:4])
            if year not in self.year_list:
                self.year_list.append(year)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
