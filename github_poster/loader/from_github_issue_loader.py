import pendulum
from github import Github

from github_poster.loader.base_loader import BaseLoader


class GitHubIssuesLoader(BaseLoader):
    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.issue_number = int(kwargs.get("issue_number", "1"))
        self.repo_name = kwargs.get("repo_name", "")
        # for private repo
        self.token = kwargs.get("github_token", "")

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--issue_number",
            dest="issue_number",
            type=str,
            required=True,
            help="The issue number",
        )
        parser.add_argument(
            "--repo_name",
            dest="repo_name",
            type=str,
            required=True,
            help="The repo name",
        )
        parser.add_argument(
            "--github_token",
            dest="github_token",
            type=str,
            default="",
            help="The GitHub token, required by private repo",
        )

    @staticmethod
    def __map_func(comment):
        data = comment.body.splitlines()[0]
        try:
            return int(data)
        except (ValueError, TypeError):
            return 0

    def get_api_data(self):
        if self.token:
            u = Github(self.token)
            me = u.get_user().login
        else:
            u = Github()
            me = "someone"
        repo = u.get_repo(self.repo_name)
        comments = repo.get_issue(self.issue_number).get_comments()
        for c in comments:
            if (
                c.user.login == me
                and pendulum.instance(c.created_at).in_timezone(self.time_zone).year
                in self.year_list
            ):
                yield c

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
                self.number_by_date_dict[date_str] += number
                self.number_list.append(number)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
