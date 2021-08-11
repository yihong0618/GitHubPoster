#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

from github_poster.loader.base_loader import BaseLoader


class MutipleLoader(BaseLoader):
    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.types = kwargs.get("types", "")
        self.type_summary_dict = {}
        self.loader_list = []

    def set_loader_list(self, loader):
        self.loader_list.append(loader)

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--types",
            dest="types",
            type=str,
            required=True,
            help="All types you want to ",
        )
        parser.add_argument(
            "--twitter_user_name",
            dest="twitter_user_name",
            type=str,
            help="twitter_user_name",
        )
        parser.add_argument(
            "--github_user_name",
            dest="github_user_name",
            type=str,
            help="github_user_name",
        )
        parser.add_argument(
            "--dota2_id",
            dest="dota2_id",
            type=str,
            help="dota2 id",
        )
        parser.add_argument(
            "--leetcode_cookie",
            dest="leetcode_cookie",
            type=str,
            help="",
        )
        parser.add_argument(
            "--cn",
            dest="cn",
            action="store_true",
            help="if accout is CN",
        )
        parser.add_argument(
            "--ns_device_id",
            dest="ns_device_id",
            type=str,
            help="",
        )
        parser.add_argument(
            "--ns_session_token",
            dest="ns_session_token",
            type=str,
            help="",
        )
        parser.add_argument(
            "--strava_client_id",
            dest="strava_client_id",
            type=str,
            help="",
        )
        parser.add_argument(
            "--strava_client_secret",
            dest="strava_client_secret",
            type=str,
            help="",
        )
        parser.add_argument(
            "--strava_refresh_token",
            dest="strava_refresh_token",
            type=str,
            help="",
        )
        parser.add_argument(
            "--wakatime_key",
            dest="wakatime_key",
            type=str,
            help="your wakatime api key here, "
            "more info: https://wakatime.com/settings/api-key",
        )
        parser.add_argument(
            "--gpx_dir",
            dest="gpx_dir",
            metavar="DIR",
            type=str,
            default="GPX_FOLDER",
            help="Directory containing GPX files",
        )
        # for gitlab
        parser.add_argument(
            "--gitlab_user_name",
            dest="gitlab_user_name",
            type=str,
            help="",
        )

        parser.add_argument(
            "--base_url",
            dest="base_url",
            type=str,
            default="https://gitlab.com",
            help="specify the base url of your self-managed gitlab",
        )
        parser.add_argument(
            "--session",
            dest="session",
            type=str,
            default="",
            help="use gitlab_session from Cookies "
            "if your gitlab instance needs to sign in",
        )

        # github issue
        parser.add_argument(
            "--issue_number",
            dest="issue_number",
            type=str,
            help="The issue number",
        )
        parser.add_argument(
            "--repo_name",
            dest="repo_name",
            type=str,
            help="The repo name",
        )
        parser.add_argument(
            "--github_token",
            dest="github_token",
            type=str,
            default="",
            help="The GitHub token, required by private repo",
        )
        # duolingo
        parser.add_argument(
            "--duolingo_user_name",
            dest="duolingo_user_name",
            type=str,
            help="",
        )

        # cichang
        parser.add_argument(
            "--cichang_user_name",
            dest="cichang_user_name",
            type=str,
            help="The username of CiChang",
        )
        parser.add_argument(
            "--cichang_password",
            dest="cichang_password",
            type=str,
            help="The password of CiChang",
        )
        # bilibili
        parser.add_argument(
            "--bilibili_cookie",
            dest="bilibili_cookie",
            type=str,
            help="The cookie for the bilibili website(XHR)",
        )
        # nrc
        parser.add_argument(
            "--nike_refresh_token",
            dest="nike_refresh_token",
            type=str,
            help="",
        )
        # garmin
        parser.add_argument(
            "--garmin_user_name",
            dest="garmin_user_name",
            type=str,
            help="The username of Garmin",
        )
        parser.add_argument(
            "--garmin_password",
            dest="garmin_password",
            type=str,
            help="The password of Garmin",
        )

    def get_api_data(self):
        pass

    def make_track_dict(self):
        pass

    def get_all_track_data(self):
        """
        date_summary_dict:
        -> {date: {github:1, twitter:2}, date2: {github: 2}}
        """
        date_summary_dict = defaultdict(dict)
        for loader in self.loader_list:
            data, _ = loader.get_all_track_data()
            for date, value in data.items():
                date_summary_dict[date][loader._type] = value
        return date_summary_dict, self.year_list
