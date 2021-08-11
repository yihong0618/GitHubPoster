import datetime
import json
import time
from collections import defaultdict

import requests

from github_poster.loader.base_loader import BaseLoader
from github_poster.loader.config import (
    NIKE_BASE_URL,
    NIKE_CLIENT_ID,
    NIKE_TOKEN_REFRESH_URL,
)


class NRCLoader(BaseLoader):
    track_color = "#F4ED5E"
    unit = "km"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.session = requests.Session()
        self.before = None
        self.after = None
        self.number_by_date_dict = defaultdict(float)
        self.nike_access = False
        self.nike_refresh_token = kwargs.get("nike_refresh_token", "")

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--nike_refresh_token",
            dest="nike_refresh_token",
            type=str,
            required=True,
            help="",
        )

    def _get_access(self):
        try:
            r = self.session.post(
                NIKE_TOKEN_REFRESH_URL,
                data=json.dumps(
                    {
                        "refresh_token": self.nike_refresh_token,
                        "client_id": NIKE_CLIENT_ID,
                        "grant_type": "refresh_token",
                    }
                ),
            )
        except Exception as e:
            print(str(e))
            raise Exception("Nike Auth failed please check your refresh token")
        access_token = r.json()["access_token"]
        self.session.headers.update({"Authorization": f"Bearer {access_token}"})

    def get_api_data(self, timestamp=0):
        if not self.nike_access:
            self._get_access()

        last_id = None
        while True:
            if last_id is not None:
                url = f"{NIKE_BASE_URL}/activities/after_id/{last_id}"
            else:
                url = f"{NIKE_BASE_URL}/activities/after_time/{timestamp}"
            r = self.session.get(url)
            if not r.ok:
                raise Exception("Get activities failed")
            data = r.json()
            last_id = data["paging"].get("after_id")
            activities = data["activities"]
            print(f"get NRC data since id {last_id}")

            for activity in activities:
                # ignore NTC record
                app_id = activity["app_id"]
                if app_id == "com.nike.ntc.brand.ios":
                    continue
                yield activity
            if last_id is None or not activities:
                return

    def make_track_dict(self):
        try:
            timestamp = int(
                time.mktime(
                    datetime.datetime.strptime(
                        f"01/01/{self.from_year}", "%d/%m/%Y"
                    ).timetuple()
                )
                * 1000
            )
        except Exception as e:
            print(str(e))
            timestamp = 0
        tracks = list(self.get_api_data(timestamp))
        for t in tracks:
            start_time = t["start_epoch_ms"]
            start_date = str(datetime.datetime.fromtimestamp(start_time / 1000).date())
            summaries = t["summaries"]
            distance = 0.0
            for summary in summaries:
                if summary.get("metric", "") == "distance":
                    distance = summary["value"]
                    distance = round(distance, 2)
                    self.number_by_date_dict[start_date] += distance
                    break
            self.number_list.append(distance)
        return tracks

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
