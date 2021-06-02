import os
import json
from collections import defaultdict

import pendulum
from .base_loader import BaseLoader
from .config import GPX_ACTIVITY_NAME_TUPLE


class YouTubeLoader(BaseLoader):
    def __init__(self, from_year, to_year, **kwargs) -> None:
        super().__init__()
        assert to_year >= from_year
        self.from_year = from_year
        self.to_year = to_year
        self.number_by_date_dict = defaultdict(int)
        self.input_dir = kwargs.get("input_dir", "")
        self.youtube_file = kwargs.get("youtube_file", "")
        self._make_years_list()

    def _parse_youtube_history(self):
        base_file = os.path.join(self.input_dir, self.youtube_file)
        data_list = []
        with open(base_file) as f:
            data_list = json.load(f)
        return data_list

    def get_api_data(self):
        return self._parse_youtube_history()

    def make_track_dict(self):
        tracks = self.get_api_data()
        for t in tracks:
            date_time = pendulum.parse(t["time"], tz=self.time_zone)
            if date_time.year < self.from_year:
                break
            date = date_time.to_date_string()
            self.number_by_date_dict[date] += 1
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)
        return tracks

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
