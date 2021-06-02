from parser import GitHubParser

import requests
from .base_loader import BaseLoader
from .config import GITHUB_CONTRIBUCTIONS_URL


class GitHubLoader(BaseLoader):
    def __init__(self, from_year, to_year, **kwargs) -> None:
        super().__init__()
        assert to_year >= from_year
        self.from_year = from_year
        self.to_year = to_year
        self.user_name = kwargs.get("github_user_name", "")
        self._make_years_list()

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
                raise Exception(f"Can not get GitHub contribuctions error: {str(e)}")
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
