from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime

import pendulum
import pytz

from github_poster.loader.config import TIME_ZONE


class LoadError(Exception):
    pass


class BaseLoader(ABC):

    #: The track color of the poster
    track_color = None
    #: The unit used by the poster
    unit = "times"

    def __init__(self, from_year, to_year, _type, **kwargs):
        assert to_year >= from_year
        self.from_year = from_year
        self.to_year = to_year
        self._type = _type
        self.time_zone = TIME_ZONE
        self.number_by_date_dict = defaultdict(int)
        self.special_number1 = None
        self.special_number2 = None
        self.number_list = []
        self.year_list = self._make_years_list()

    def _make_years_list(self):
        return list(range(int(self.from_year), int(self.to_year) + 1))

    def make_month_list(self):
        start = pendulum.datetime(self.from_year, 1, 1)
        end = pendulum.datetime(self.to_year, 12, 31)
        period = pendulum.period(start, end)
        month_list = list(period.range("months"))
        # filter
        month_list = [m for m in month_list if m < pendulum.now()]
        return month_list

    def make_special_number(self):
        """
        This func is to make special color number for poster
        special_number1 top 20%
        special_number2  top 20 % - 50%
        """
        # before python below 3.5 maybe need to sort
        number_list_set = sorted(list(set(self.number_list)))
        number_list_set_len = len(number_list_set)
        if number_list_set_len < 3:
            self.special_number1 = self.special_number2 = float("inf")
            return
        elif len(self.number_list) < 10:
            self.special_number1 = number_list_set[-1]
            self.special_number2 = number_list_set[-2]
        else:
            self.special_number1 = number_list_set[-1 * int(number_list_set_len * 0.2)]
            self.special_number2 = number_list_set[-1 * int(number_list_set_len * 0.50)]

    def adjust_time(self, time):
        tc_offset = datetime.now(pytz.timezone(self.time_zone)).utcoffset()
        return time + tc_offset

    @classmethod
    def add_arguments(cls, parser):
        loader_group = parser.add_argument_group("Loader Arguments")
        cls.add_loader_arguments(loader_group)
        group = parser.add_argument_group("Common Arguments")
        group.add_argument(
            "--year",
            metavar="YEAR",
            type=str,
            default=str(datetime.now().year),
            help='Filter tracks by year; "NUM", "NUM-NUM", "all" (default: all years)',
        )
        group.add_argument(
            "--me",
            metavar="NAME",
            type=str,
            default="Joey",
            help='User name to display (default: "Joey").',
        )
        group.add_argument(
            "--background-color",
            dest="background_color",
            metavar="COLOR",
            type=str,
            default="#222222",
            help='Background color of poster (default: "#222222").',
        )
        group.add_argument(
            "--track-color",
            dest="track_color",
            metavar="COLOR",
            type=str,
            default="#4DD2FF",
            help='Color of tracks (default: "#4DD2FF").',
        )
        group.add_argument(
            "--text-color",
            dest="text_color",
            metavar="COLOR",
            type=str,
            default="#FFFFFF",
            help='Color of text (default: "#FFFFFF").',
        )
        group.add_argument(
            "--special-color1",
            dest="special_color1",
            metavar="COLOR",
            default="yellow",
            help='Special track color (default: "yellow").',
        )
        group.add_argument(
            "--special-color2",
            dest="special_color2",
            metavar="COLOR",
            default="red",
            help="Secondary color of special tracks (default: red).",
        )
        group.add_argument(
            "--special-number1",
            dest="special_number1",
            type=float,
            default=0,
            help="Special number 1",
        )
        group.add_argument(
            "--special-number2",
            dest="special_number2",
            type=float,
            default=0,
            help="Special number 2",
        )
        group.add_argument(
            "--with-animation",
            dest="with_animation",
            action="store_true",
            help="add animation to the poster",
        )
        group.add_argument(
            "--animation-time",
            dest="animation_time",
            type=int,
            default=10,
            help="animation duration (default: 10s)",
        )
        # skyline args here
        group.add_argument(
            "--with-skyline",
            dest="with_skyline",
            action="store_true",
            help="with skyline(stl file)",
        )
        group.add_argument(
            "--skyline-with-name",
            dest="skyline_with_name",
            action="store_true",
            help="print name on skyline",
        )
        group.add_argument(
            "--skyline-year",
            dest="skyline_year",
            type=str,
            default="",
            help="the year to generate skyline",
        )
        # circular args here
        group.add_argument(
            "--is-circular",
            dest="is_circular",
            action="store_true",
            help="if is circular poster",
        )

    @classmethod
    def add_loader_arguments(cls, parser):
        pass

    @abstractmethod
    def make_track_dict(self):
        pass

    @abstractmethod
    def get_all_track_data(self):
        pass
