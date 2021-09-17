import math
import os

import numpy as np
from pendulum import parse, period
from sdf import X, Y, box, ease, measure_text, rectangle, text, union

import github_poster.skyline
from github_poster.skyline.config import (
    BASE_HEIGHT,
    BASE_LENGTH,
    BASE_TOP_LENGTH,
    BASE_TOP_WIDTH,
    BASE_WIDTH,
    BOX_DIMENSION,
)


class Skyline:
    def __init__(self, file_name, year, skyline_type, number_by_date_dict, user_name):
        self.file_name = file_name
        self.year = year
        self.skyline_type = skyline_type
        self.number_by_date_dict = number_by_date_dict
        self.type_info_dict = None
        assert len(user_name) < 16
        self.user_name = user_name

    def _make_box(self, box_height):
        b = box((BOX_DIMENSION, BOX_DIMENSION, box_height))
        # change to the base location
        b = b.translate(
            (BOX_DIMENSION / 2, BOX_DIMENSION / 2, box_height / 2 + BASE_HEIGHT)
        )
        return b

    def __make_one_year_dates(self):
        dates = list(period(parse(f"{self.year}-01-01"), parse(f"{self.year}-12-31")))
        return [d.to_date_string() for d in dates]

    def _make_skyline_boxes(self):
        box_list = []
        dates = self.__make_one_year_dates()
        # for test
        week_number = 0
        for i, j in enumerate(dates):
            day_number = i % 7
            if day_number == 0:
                week_number += 1
            value = self.number_by_date_dict.get(j)
            if value:
                box = self._make_box(value)
                box = box.translate(
                    (
                        3.5 + 2.5 + (week_number - 1) * BOX_DIMENSION,
                        3.5 + 2.5 + day_number * BOX_DIMENSION,
                        0,
                    )
                )
                box_list.append(box)
        return box_list

    def _make_skyline_card(self, text_info, offset=0):
        # TODO change the magic numbers
        # support change font
        FONT = os.path.join(github_poster.skyline.__path__[0], "font", "arial.ttf")
        TEXT = text_info
        w, h = measure_text(FONT, TEXT)
        t = (
            text(FONT, TEXT, 5 * (w / h), 5)
            .extrude(h)
            .translate((10 + w + offset, BASE_HEIGHT / 2, h / 2))
        )
        face_angle = math.tan(3.5 / 10)
        t = t.orient(Y).rotate(-face_angle, X)
        return t

    def _make_skyline_base(self):
        base = rectangle((BASE_LENGTH, BASE_WIDTH)).extrude_to(
            rectangle((BASE_TOP_LENGTH, BASE_TOP_WIDTH)), BASE_HEIGHT, ease.linear
        )
        # change to the base location
        base = base.translate((BASE_TOP_LENGTH / 2, BASE_WIDTH / 2, BASE_HEIGHT / 2))
        return base

    def _normalize_data(self):
        """
        normalize the values from 1 to 20
        """
        if self.number_by_date_dict:
            values_list = list(self.number_by_date_dict.values())
            values_list = (values_list - np.min(values_list)) / (
                np.max(values_list) - np.min(values_list)
            )
            values_list = [int(i * 20) + 1 for i in values_list]
            # only support for Python 3.6+, dict is ordered
            self.number_by_date_dict = dict(
                zip(self.number_by_date_dict.keys(), values_list)
            )

    def make_skyline(self):
        self._normalize_data()
        base = self._make_skyline_base()
        boxes = self._make_skyline_boxes()
        boxes = union(*boxes)
        text_info = self.type_info_dict.get(self.skyline_type, self.skyline_type)
        skyline_info_card = self._make_skyline_card(text_info)
        skyline_year_card = self._make_skyline_card(str(self.year), offset=120)
        skyline = base | boxes | skyline_info_card.k(0.25) | skyline_year_card.k(0.25)
        if self.user_name:
            skyline_name_card = self._make_skyline_card(self.user_name, offset=30)
            skyline = skyline | skyline_name_card
        skyline.save(self.file_name)
