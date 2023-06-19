import time

import requests

from github_poster.loader.base_loader import BaseLoader
from github_poster.loader.config import SHANBAY_WORD_API


class ShanBayLoader(BaseLoader):
    track_color = "#ADD8E6"
    unit = "words"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.user_name = kwargs.get("shanbay_user_name", "")

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--shanbay_user_name",
            dest="shanbay_user_name",
            type=str,
            required=optional,
            help="",
        )

    def get_api_data(self):
        err_counter = 0
        page = 1
        datalist = []
        while err_counter < 10:
            url = SHANBAY_WORD_API.format(user_name=self.user_name, page=page)
            res = requests.get(url)

            if not res.ok:
                print(f"get shanbay word api failed {str(res.text)}")
                err_counter += 1
                continue

            data = res.json()
            if "objects" not in data or "ipp" not in data:
                print(f"unknown payload: {data}")
                err_counter += 1

            objects = data["objects"]
            datalist = datalist + objects
            ipp = data["ipp"] or 20
            if len(objects) < ipp:
                break
            date = objects[-1]["date"]
            year = int(date[0:4])
            if year < self.from_year:
                break

            page += 1
            time.sleep(0.5)

        return datalist

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            n_words = sum(self.convert_to_int(i["num"]) for i in d["tasks"])
            self.number_by_date_dict[d["date"]] = n_words
            self.number_list.append(n_words)

    def convert_to_int(self, num):
        """
        处理num为字符串的情况,扇贝的API返回的数据可能会不一致,num的值可能为:
        num: 50 或 num: "50", 这里把字符串做一次转换
        """
        try:
            return int(num)
        except Exception:
            return 0

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
