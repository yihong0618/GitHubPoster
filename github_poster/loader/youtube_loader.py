import json
from collections import defaultdict

import pendulum

from github_poster.loader.base_loader import BaseLoader


class YouTubeLoader(BaseLoader):
    track_color = "#FFFFFF"
    unit = "videos"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.number_by_date_dict = defaultdict(int)
        self.youtube_file = kwargs.get("youtube_history_file_file")

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--youtube_history_file_file",
            dest="youtube_history_file",
            type=str,
            default="IN_FOLDER/watch-history.json",
            help="youtube history file path",
        )

    def _parse_youtube_history(self):
        base_file = self.youtube_file
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
