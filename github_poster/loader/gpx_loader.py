import datetime
import os
from collections import defaultdict

import gpxpy

from github_poster.loader.base_loader import BaseLoader, LoadError
from github_poster.loader.config import GPX_ACTIVITY_NAME_TUPLE


class GPXLoader(BaseLoader):
    unit = "km"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.number_by_date_dict = defaultdict(float)
        self.before = None
        self.after = None
        self.base_dir = kwargs.get("gpx_dir", "")

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--gpx_dir",
            dest="gpx_dir",
            metavar="DIR",
            type=str,
            default="GPX_FOLDER",
            help="Directory containing GPX files",
        )

    def _make_year_before_after(self):
        self.before = datetime.datetime(int(self.to_year) + 1, 1, 1)
        self.after = datetime.datetime(int(self.from_year), 1, 1)

    def _list_gpx_files(self):
        base_dir = os.path.abspath(self.base_dir)
        if not os.path.isdir(base_dir):
            raise LoadError(f"Not a directory: {base_dir}")
        for name in os.listdir(base_dir):
            if name.startswith("."):
                continue
            path_name = os.path.join(base_dir, name)
            if name.endswith(".gpx") and os.path.isfile(path_name):
                yield path_name

    def __parse_gpx(self, file_name):
        with open(file_name) as f:
            gpx = gpxpy.parse(f)
            try:
                start_time, _ = gpx.get_time_bounds()
                # timezone offset
                start_time = self.adjust_time(start_time)
                distance = gpx.length_2d()
            except Exception as e:
                print(f"Something is wrong when loading file {file_name}", str(e))
        return start_time.date(), distance

    def get_api_data(self):
        self._make_year_before_after()
        files = list(self._list_gpx_files())
        print("Loading your gpx files it may take a little time please wait")
        for f in files:
            date, distance = self.__parse_gpx(f)
            # filter
            if date.year < self.from_year or date.year > self.to_year:
                continue
            yield GPX_ACTIVITY_NAME_TUPLE(date, distance)

    def make_track_dict(self):
        tracks = list(self.get_api_data())
        for t in tracks:
            num = round(float(t.distance) / 1000, 2)
            self.number_by_date_dict[str(t.date)] += num
            self.number_list.append(num)
        return tracks

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
