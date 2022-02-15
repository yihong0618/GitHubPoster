#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

from github_poster.loader.base_loader import BaseLoader


class MultipleLoader(BaseLoader):
    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.types = kwargs.get("types", "")
        self.type_summary_dict = {}
        self.loader_list = []

    def set_loader_list(self, loader):
        self.loader_list.append(loader)

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--types",
            dest="types",
            type=str,
            required=True,
            help="All types you want to generate summary, split by comma",
        )
        for loader in cls.parser_loader_list:
            loader.add_loader_arguments(parser, optional)

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
