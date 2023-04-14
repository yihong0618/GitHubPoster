import json
import os
from collections import defaultdict

import pendulum

from github_poster.loader.base_loader import BaseLoader


class ChatGPTLoader(BaseLoader):
    track_color = "#70A597"
    unit = "times"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.number_by_date_dict = defaultdict(int)
        self.youtube_file = kwargs.get("chatgpt_history_file")

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--chatgpt_history_file",
            dest="chatgpt_history_file",
            type=str,
            default=os.path.join("IN_FOLDER", "chatgpt-history.json"),
            help="chatgpt history file path",
        )

    def _parse_chatgpt_history(self):
        base_file = self.youtube_file
        data_list = []
        with open(base_file) as f:
            data_list = json.load(f)
        return data_list

    def get_api_data(self):
        return self._parse_chatgpt_history()

    def make_track_dict(self):
        tracks = self.get_api_data()
        for data in tracks:
            user_ask_list = []
            for key in data["mapping"]:
                if (
                    "message" in data["mapping"][key]
                    and data["mapping"][key]["message"] is not None
                ):
                    message = data["mapping"][key]["message"]
                    if "author" in message and message["author"]["role"] == "user":
                        user_ask_list.append(message)
            for ask in user_ask_list:
                date_time = pendulum.from_timestamp(
                    int(ask["create_time"]), tz=self.time_zone
                )
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
