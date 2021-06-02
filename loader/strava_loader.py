import datetime
from collections import defaultdict

import stravalib

from .base_loader import BaseLoader


class StravaLoader(BaseLoader):
    def __init__(self, from_year, to_year, **kwargs) -> None:
        super().__init__()
        assert to_year >= from_year
        self.from_year = from_year
        self.to_year = to_year
        self.before = None
        self.after = None
        self.number_by_date_dict = defaultdict(float)
        self.client = stravalib.Client()
        self.client_id = kwargs.get("strava_client_id", "")
        self.client_secret = kwargs.get("strava_client_secret", "")
        self.refresh_token = kwargs.get("strava_refresh_token", "")
        self.strava_access = False
        self._make_years_list()

    def _make_year_before_after(self):
        self.before = datetime.datetime(int(self.to_year) + 1, 1, 1)
        self.after = datetime.datetime(int(self.from_year), 1, 1)

    def _get_access(self):
        try:
            response = self.client.refresh_access_token(
                client_id=self.client_id,
                client_secret=self.client_secret,
                refresh_token=self.refresh_token,
            )
        except:
            raise Exception("Something is wrong with your auth please check")

        self.access_token = response["access_token"]
        self.refresh_token = response["refresh_token"]
        self.client.access_token = response["access_token"]
        self.strava_access = True

    def get_api_data(self):
        if not self.strava_access:
            self._get_access()
        # make year range
        self._make_year_before_after()
        return self.client.get_activities(before=self.before, after=self.after)

    def make_track_dict(self):
        tracks = list(self.get_api_data())
        for t in tracks:
            num = round(float(t.distance) / 1000, 2)
            self.number_by_date_dict[str(t.start_date_local.date())] += num
            self.number_list.append(num)
        return tracks

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
