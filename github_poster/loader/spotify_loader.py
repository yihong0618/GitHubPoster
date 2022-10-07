import datetime
import json
import os
import time
from base64 import urlsafe_b64encode
from collections import defaultdict

import requests

from github_poster.loader.base_loader import BaseLoader, LoadError
from github_poster.loader.config import SPOTIFY_HISTORY_URL, SPOTIFY_TOKEN


class SpotifyLoader(BaseLoader):
    track_color = "#FFE411"
    unit = "songs"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.number_by_date_dict = defaultdict(int)
        self.session = requests.Session()
        self.client_id = kwargs.get("spotify_client_id", "")
        self.client_secret = kwargs.get("spotify_client_secret", "")
        self.refresh_token = kwargs.get("spotify_refresh_token", "")
        self.access_token = ""
        self.spotify_file = kwargs.get("spotify_history_file")
        self._parse_spotify_history()

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--spotify_client_id",
            dest="spotify_client_id",
            type=str,
            required=optional,
            help="",
        )
        parser.add_argument(
            "--spotify_client_secret",
            dest="spotify_client_secret",
            type=str,
            required=optional,
            help="",
        )
        parser.add_argument(
            "--spotify_refresh_token",
            dest="spotify_refresh_token",
            type=str,
            required=optional,
            help="",
        )
        parser.add_argument(
            "--spotify_history_file",
            dest="spotify_history_file",
            type=str,
            default=os.path.join("IN_FOLDER", "spotify-history.json"),
            help="spotify history file path",
        )

    def _parse_spotify_history(self):
        if os.path.exists(self.spotify_file):
            with open(self.spotify_file, "r") as f:
                self.number_by_date_dict = json.load(f)

    def _writeback_spotify_history(self):
        with open(self.spotify_file, "w") as f:
            json.dump(self.number_by_date_dict, f, sort_keys=True)

    def _set_time(self):
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(
            1,
            hours=now.hour,
            minutes=now.minute,
            seconds=now.second,
            microseconds=now.microsecond,
        )
        last_yesterday = yesterday + datetime.timedelta(
            hours=23, minutes=59, seconds=59
        )
        # print(f"after: {yesterday} and before: {last_yesterday}")
        after = int(time.mktime(yesterday.timetuple()) * 1000)
        before = int(time.mktime(last_yesterday.timetuple()) * 1000)
        return after, before

    def _refresh_access_token(self):
        form = {"grant_type": "refresh_token", "refresh_token": self.refresh_token}
        authorization = f"Basic {urlsafe_b64encode(str.encode(f'{self.client_id}:{self.client_secret}')).decode()}"
        r = self.session.post(
            SPOTIFY_TOKEN,
            data=form,
            json=True,
            headers={
                "Authorization": authorization,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        if not r.ok:
            raise LoadError(
                "Can not get spotify access_token, please check your refresh_token"
            )
        self.access_token = r.json()["access_token"]

    def get_api_data(self, url, after, limit=20, data_list=[]):
        r = self.session.get(
            url,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )
        if not r.ok:
            raise LoadError(
                "Can not get spotify history data, please check your access_token"
            )
        track_list = r.json()
        # print(f'''size: {len(track_list['items'])}''')
        for i in track_list["items"]:
            track = i["track"]
            play_time = i["played_at"]
            date = datetime.datetime.strptime(
                play_time.replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S.%f"
            ) + datetime.timedelta(hours=8)
            data = f"""{date}, song: {track['name']}, artist: {track['artists'][0]['name']}, album {track['album']['name']}"""
            if time.mktime(date.timetuple()) * 1000 < after:
                continue
            data_list.append(data)

        next_url = track_list["next"]
        before = int(track_list["cursors"]["before"])
        # date_time = datetime.datetime.fromtimestamp(before//1000)
        # print(date_time.strftime('%Y-%m-%d %H:%M:%S'))
        if before >= after:
            return self.get_api_data(next_url, after, limit, data_list)
        return data_list

    def make_track_dict(self):
        self._refresh_access_token()
        after, before = self._set_time()
        url = SPOTIFY_HISTORY_URL.format(limit=20, before=before)
        data_list = self.get_api_data(url, after)
        day_map = map(lambda x: x.split()[0], data_list)
        day = set(day_map)
        assert len(day) == 1
        for i in day:
            self.number_by_date_dict[i] = len(data_list)
        # print(self.number_by_date_dict)
        self._writeback_spotify_history()

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
