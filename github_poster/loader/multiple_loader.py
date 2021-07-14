#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

from github_poster.loader.base_loader import BaseLoader


class MutipleLoader(BaseLoader):
    track_color = "#567433"
    unit = "games"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.types = kwargs.get("types", "")
        self.dota2_id = kwargs.get("id", "")
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
