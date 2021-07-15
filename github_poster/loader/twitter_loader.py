import twint

from github_poster.loader.base_loader import BaseLoader


class TwitterLoader(BaseLoader):
    track_color = "#1C9CEA"
    unit = "tweets"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.user_name = kwargs.get("twitter_user_name", "")
        self.c = twint.Config()

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--twitter_user_name",
            dest="twitter_user_name",
            type=str,
            required=True,
            help="",
        )

    def get_api_data(self):
        self.c.Username = self.user_name
        self.c.Custom["tweet"] = ["id"]
        self.c.Custom["user"] = ["bio"]
        self.c.Store_object = True
        self.c.Since = f"{self.from_year}-01-01"
        self.c.Until = f"{self.to_year}-12-31"
        twint.run.Search(self.c)
        return twint.output.tweets_list

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            date_str = d.datetime[:10]
            self.number_by_date_dict[date_str] += 1
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
