import requests

from github_poster.html_parser import GitHubParser
from github_poster.loader.base_loader import BaseLoader, LoadError
from github_poster.loader.config import GITHUB_CONTRIBUCTIONS_URL


class GitHubLoader(BaseLoader):
    track_color = "#9BE9A8"
    unit = "cons"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.user_name = kwargs.get("github_user_name", "")

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--github_user_name",
            dest="github_user_name",
            type=str,
            required=True,
            help="",
        )

    def make_track_dict(self):
        for y in self.year_list:
            p = GitHubParser()
            try:
                r = requests.get(
                    GITHUB_CONTRIBUCTIONS_URL.format(
                        user_name=self.user_name,
                        start_day=f"{y}-01-01",
                        end_day=f"{y}-12-31",
                    )
                )
                self.number_by_date_dict.update(p.make_contribution_dict(r.text))
            except Exception as e:
                raise LoadError(f"Can not get GitHub contribuctions error: {str(e)}")
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
