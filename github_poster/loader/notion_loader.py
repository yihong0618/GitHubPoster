import time
from collections import defaultdict

import pendulum
import requests

from github_poster.loader.base_loader import BaseLoader, LoadError
from github_poster.loader.config import NOTION_API_URL, NOTION_API_VERSION


class NotionLoader(BaseLoader):
    track_color = "#40C463"
    unit = "times"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.number_by_date_dict = defaultdict(int)
        self.notion_token = kwargs.get("notion_token", "")
        self.database_id = kwargs.get("database_id", "")
        self.prop_name = kwargs.get("prop_name", "")

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--notion_token",
            dest="notion_token",
            type=str,
            help="The Notion internal integration token.",
        )
        parser.add_argument(
            "--database_id",
            dest="database_id",
            type=str,
            help="The Notion database id.",
        )
        parser.add_argument(
            "--prop_name",
            dest="prop_name",
            type=str,
            default="Datetime",
            required=optional,
            help="The database property name which stored the datetime.",
        )

    def get_api_data(self, start_cursor="", page_size=100, data_list=[]):

        payload = {"page_size": page_size}
        if start_cursor:
            payload.update({"start_cursor": start_cursor})

        headers = {
            "Accept": "application/json",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.notion_token,
        }

        resp = requests.post(
            NOTION_API_URL.format(database_id=self.database_id),
            json=payload,
            headers=headers,
        )

        if not resp.ok:
            raise LoadError("Can not get Notion data, please check your config")
        data = resp.json()
        results = data["results"]
        next_cursor = data["next_cursor"]
        data_list.extend(results)
        if not data["has_more"]:
            return data_list
        # Avoid request limits
        # The rate limit for incoming requests is an average
        # of 3 requests per second.
        # See https://developers.notion.com/reference/request-limits
        time.sleep(0.3)
        return self.get_api_data(
            start_cursor=next_cursor, page_size=page_size, data_list=data_list
        )

    def make_track_dict(self):
        data_list = self.get_api_data()
        for result in data_list:
            dt = result["properties"][self.prop_name]["date"]["start"]
            date_str = pendulum.parse(dt).to_date_string()
            self.number_by_date_dict[date_str] += 1
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
