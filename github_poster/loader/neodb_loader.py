import requests

from github_poster.loader.base_loader import BaseLoader, LoadError
from github_poster.loader.config import NEODB_API


class NeoDBLoader(BaseLoader):
    unit = "Marks"
    # track_color = "#78C800"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type, **kwargs)
        self.neodb_token = kwargs.get("neodb_token", "")
        self.mark_type = kwargs.get("mark_type", "complete")

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--neodb_token",
            dest="neodb_token",
            type=str,
            help="Get token from https://neodb.social/developer",
            required=optional,
        )
        parser.add_argument(
            "--mark_type",
            dest="mark_type",
            type=str,
            help="The type of marks you want to show, like 'complete', 'wishlist', 'progress'",
            required=optional,
            default="complete",
        )

    def get_api_data(self):
        page = 1
        count = 0
        all_count = 0
        all_page = 0

        try:
            headers = {
                "Authorization": f"Bearer {self.neodb_token}",
                "Content-Type": "application/json",
            }

            while True:
                r = requests.get(
                    url=NEODB_API.format(page=page, type=self.mark_type),
                    headers=headers,
                )

                data = r.json()

                if all_count == 0 and all_page == 0:
                    all_count = data.get("count", 0)
                    all_page = data.get("pages", 1)

                data_list = data.get("data", [])

                for marks in data_list:
                    created_time = marks["created_time"]
                    created_time = created_time.split("T")[0]
                    count += 1

                    yield created_time

                if page == all_page and count == all_count:
                    break

                page += 1

        except Exception as e:
            raise LoadError(f"get neodb api failed {str(e)}")

    def make_track_dict(self):
        if self.mark_type == "all":
            type_list = ["complete", "wishlist", "progress"]
            for _type in type_list:
                self.mark_type = _type
                self.make_track_dict()
        else:
            data_list = self.get_api_data()
            for data in data_list:
                self.number_by_date_dict[data] += 1

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
