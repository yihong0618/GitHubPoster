#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

from github_poster.loader.base_loader import BaseLoader
from github_poster.loader.bilibili_loader import BilibiliLoader
from github_poster.loader.leetcode_loader import LeetcodeLoader


class SummaryLoader(BaseLoader):
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

        for l in cls.parser_loader_list:
            l.add_loader_arguments(parser, optional)

    def get_api_data(self):
        pass

    def make_track_dict(self):
        pass

    def get_all_track_data(self):
        pass
