import json
from collections import defaultdict

from github_poster.loader.base_loader import BaseLoader


class JsonLoader(BaseLoader):
    unit = "times"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.number_by_date_dict = defaultdict(int)
        self.json_file = kwargs.get("json_file")

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--json_file",
            dest="json_file",
            type=str,
            default="data.json",
            help="json file path",
        )

    def get_api_data(self):
        pass

    def make_track_dict(self):
        with open(self.json_file, "r") as f:
            tracks = json.load(f)
        self.number_by_date_dict = tracks
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)
        return tracks

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
