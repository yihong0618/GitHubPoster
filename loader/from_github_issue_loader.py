import time

import pendulum
import requests
from github import Github

from .base_loader import BaseLoader
from .config import GITHUB_BASE_URL


class GitHubIssuesLoader(BaseLoader):
    def __init__(self, from_year, to_year, **kwargs):
        super().__init__()
        self.from_year = from_year
        self.to_year = to_year
        self.issue_number = int(kwargs.get("github_issue_number", "1"))
        self.repo_name = kwargs.get("github_repo_name", "")
        # for private repo
        self.github_token = kwargs.get("github_token", "")

    @staticmethod
    def __map_func(comment):
        data = comment.body.splitlines()[0]
        try:
            return int(data)
        except:
            return 0

    def get_api_data(self):
        self._make_years_list()
        if self.github_token:
            u = Github(self.github_token)
        else:
            u = Github()
        me = u.get_user().login
        repo = u.get_repo(self.repo_name)
        data_list = []
        comments = repo.get_issue(self.issue_number).get_comments()
        for c in comments:
            if (
                c.user.login == me
                and pendulum.instance(c.created_at).in_timezone(self.time_zone).year
                in self.year_list
            ):
                data_list.append(c)
        return data_list

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            date_str = (
                pendulum.instance(d.created_at)
                .in_timezone(self.time_zone)
                .to_date_string()
            )
            number = self.__map_func(d)
            if number:
                self.number_by_date_dict[date_str] = number
                self.number_list.append(number)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
