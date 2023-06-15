import requests,time

from github_poster.loader.base_loader import BaseLoader
from github_poster.loader.config import SHANBAY_WORD_API

#扇贝单词loader,可记录每天背诵的单词数
class ShanBayWordLoader(BaseLoader):
    track_color = "#ADD8E6"
    #special1 = '#009688'
    #special2 = '#007BFF'
    unit = "words"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.user_name = kwargs.get("shanbay_word_user_name", "")

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--shanbay_word_user_name",
            dest="shanbay_word_user_name",
            type=str,
            required=optional,
            help="",
        )
    
    def get_api_data(self):
        err_counter = 0
        page = 1
        datalist = []
        while err_counter < 10:
            url = SHANBAY_WORD_API.format(user_name=self.user_name,page=page)
            res = requests.get(url)
            
            if not res.ok:
                print(f"get shanbay word api failed {str(res.text)}")
                err_counter += 1
                continue
            
            data = res.json()
            if "objects" not in data or "ipp" not in data:
                print(f'unknown payload: {data}')
                err_counter += 1

            objects = data["objects"]
            datalist = datalist + objects
            ipp = data['ipp'] or 20
            if len(objects) < ipp:
                break
            date = objects[-1]['date']
            year = int(date[0:4])
            if year < self.from_year:
                break

            page += 1
            time.sleep(0.05)

        return datalist

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            n_words = sum(i["num"] for i in d['tasks'])
            self.number_by_date_dict[d["date"]] = n_words
            self.number_list.append(n_words)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list        