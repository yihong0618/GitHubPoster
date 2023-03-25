import pendulum as pdl
import requests

from github_poster.err import DepNotInstalledError
from github_poster.loader.base_loader import BaseLoader

try:
    import pandas as pd
except ImportError:
    pd = None


class TodoistLoader(BaseLoader):
    track_color = "#FFE411"
    unit = "tasks"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.from_year = from_year
        self.to_year = to_year
        self.todoist_token = kwargs.get("todoist_token", "")
        # another magic number, try 3 times for calling api
        self.MAXIMAL_RETRY = 3

    @classmethod
    def try_import_deps(cls):
        if pd is None:
            raise DepNotInstalledError(
                "Todoist dependencies are not installed, "
                "please use `pip3 install -U 'github_poster[todoist]'` to install."
            ) from None

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        # add argument for loader
        parser.add_argument(
            "--todoist_token",
            dest="todoist_token",
            type=str,
            required=optional,
            help="dev token",
        )

    # call with token
    def response(self, url, postdata):
        headers = {"Authorization": "Bearer {0}".format(self.todoist_token)}
        res = requests.post(url=url, data=postdata, headers=headers)
        resposn = res.json()
        return resposn

    # call with re-try since todoist api some time get 502
    def response_with_retry(self, url, postdata, times=1):
        # time.sleep(1)
        try:
            return self.response(url, postdata)
        except Exception as e:
            if times >= self.MAXIMAL_RETRY:
                print(
                    f">> Exceed maximal retry {self.MAXIMAL_RETRY}, Raise exception..."
                )
                raise (e)  # will stop the program without further handling
            else:
                times += 1
                print(f">> Exception, Retry {times} begins...")
                return self.response_with_retry(url, postdata, times)

    # call todoist dev api to get activity of completed tasks
    # refer https://developer.todoist.com/sync/v9/#activity
    def todoist_completed_activity(self, page, limit, offset):
        data = {
            "event_type": "completed",
            "page": page,
            "limit": limit,
            "offset": offset,
        }
        url = "https://api.todoist.com/sync/v9/activity/get"
        re = self.response_with_retry(url, postdata=data)
        return re

    # json expect to be list of events format
    # with event_date, event_type, id
    def normalize_df(self, jsondata):
        if jsondata["count"] == 0:
            return pd.DataFrame(columns=["event_date", "event_type", "id"])
        df = pd.json_normalize(jsondata["events"])
        df = df[["event_date", "event_type", "id"]]
        df["event_date"] = df["event_date"].str.slice(0, 10)
        return df

    def count_to_dict(self, df):
        return df.groupby(["event_date"])["event_date"].count().to_dict()

    # refer https://developer.todoist.com/sync/v9/#activity
    # todoist api only allows you to get activity data by page from current day
    # we will have to calculate the pages based on from and to year then manipulate the dict data
    def get_api_data(self):
        # init critical dates
        pdl.now().to_date_string()
        current_year = pdl.now().year
        # how many days in the range
        number_of_days = pdl.today().diff(pdl.datetime(self.from_year, 1, 1)).in_days()
        # current year
        page_from = (
            0 if current_year == self.to_year else pdl.today().timetuple().tm_yday // 7
        )
        page_to = number_of_days // 7 + 1
        print("Todoist API Page range ({0},{1})".format(page_from, page_to))
        last_day_of_to_year = pdl.datetime(self.to_year, 12, 31).to_date_string()
        first_day_of_from_year = pdl.datetime(self.from_year, 1, 1).to_date_string()

        df = pd.DataFrame(columns=["event_date", "event_type", "id"])
        # magic number 3 is to cover the 0.14 extra week of every year when counting number of pages
        for page in range(page_from, page_to + 3):
            offset = 0
            limit = 100
            while True:
                res = self.todoist_completed_activity(page, limit, offset)
                if res["count"] >= offset:
                    offset = offset + limit
                    df_res = self.normalize_df(res)
                    df = pd.concat([df, df_res])
                else:
                    break

        df = df[df["event_date"] >= first_day_of_from_year]
        df = df[df["event_date"] <= last_day_of_to_year]

        return df

    def make_track_dict(self):
        # generate statistics data
        df = self.get_api_data()
        df_dict = self.count_to_dict(df)
        self.number_by_date_dict = df_dict
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        print("不积跬步，无以至千里。Todoist欢迎你。")
        return self.number_by_date_dict, self.year_list
