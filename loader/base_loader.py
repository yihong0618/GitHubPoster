from collections import defaultdict
from abc import ABC, abstractclassmethod
from .config import TIME_ZONE
import pendulum


class BaseLoader(ABC):
    def __init__(self):
        self.from_year = None
        self.to_year = None
        self.time_zone = TIME_ZONE
        self.number_by_date_dict = defaultdict(int)
        self.special_number1 = None
        self.special_number2 = None
        self.number_list = []

    def _make_years_list(self):
        self.year_list = list(range(int(self.from_year), int(self.to_year) + 1))

    def make_month_list(self):
        start = pendulum.datetime(self.from_year, 1, 1)
        end = pendulum.datetime(self.to_year, 12, 31)
        period = pendulum.period(start, end)
        month_list = list(period.range("months"))
        return month_list

    def make_special_number(self):
        """
        This func is to make special color number for poster
        special_number1 top 10%
        special_number2  top 10 % - 25%
        """
        # before python below 3.5 maybe need to sort
        number_list_set = sorted(list(set(self.number_list)))
        number_list_set_len = len(number_list_set)
        if number_list_set_len < 5:
            return
        elif len(self.number_list) < 10:
            self.special_number1 = number_list_set[-1]
            self.special_number2 = number_list_set[-2]
        else:
            self.special_number1 = number_list_set[-1 * int(number_list_set_len * 0.2)]
            self.special_number2 = number_list_set[
                -1 * int(number_list_set_len * 0.50)
            ]

    @abstractclassmethod
    def make_track_dict(self):
        pass

    @abstractclassmethod
    def get_all_track_data(self):
        pass
