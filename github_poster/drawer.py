import calendar
import datetime

import svgwrite

from github_poster.config import (
    COLOR_TUPLE,
    DEFAULT_DOM_COLOR,
    DOM_BOX_DICT,
    DOM_BOX_TUPLE,
    MONTH_NAMES,
)
from github_poster.err import BaseDrawError
from github_poster.utils import interpolate_color, make_key_times


class Drawer:

    name = "github"

    def __init__(self, p):
        self.poster = p

    @property
    def type_color_dict(self):
        """
        for multiple types
        """
        return dict(
            zip(self.poster.type_list, COLOR_TUPLE[: len(self.poster.type_list)])
        )

    def make_color(self, length_range, length):
        has_special = (
            self.poster.special_number["special_number2"]
            < length
            < self.poster.special_number["special_number1"]
        )
        color_from = (
            self.poster.colors["special"]
            if has_special
            else self.poster.colors["track"]
        )
        color_to = self.poster.colors["special2"]
        diff = length_range.diameter()
        if diff == 0:
            return color_from

        return interpolate_color(
            color_from, color_to, (length - length_range.lower()) / diff
        )

    def __add_animation(self, rect, key_times, animate_index):
        values = (
            ";".join(["0"] * animate_index)
            + ";"
            + ";".join(["1"] * (len(key_times) - animate_index))
        )
        rect.add(
            svgwrite.animate.Animate(
                "opacity",
                dur=f"{self.poster.animation_time}s",
                values=values,
                keyTimes=";".join(key_times),
                repeatCount="1",
            )
        )
        return rect

    def _gen_day_box(
        self,
        dr,
        rect_x,
        rect_y,
        date_title,
        day_tracks,
        with_animation,
        key_times,
        animate_index,
    ):
        color = DEFAULT_DOM_COLOR
        if day_tracks:
            color = self.make_color(self.poster.length_range_by_date, day_tracks)
            if day_tracks >= self.poster.special_number["special_number1"]:
                color = self.poster.colors.get("special2") or self.poster.colors.get(
                    "special"
                )
            date_title = f"{date_title} {day_tracks} {self.poster.units}"
        rect = dr.rect((rect_x, rect_y), DOM_BOX_TUPLE, fill=color)
        if with_animation:
            rect = self.__add_animation(rect, key_times, animate_index)
        rect.set_desc(title=date_title)
        yield rect

    def _gen_day_boxes(
        self,
        dr,
        rect_x,
        rect_y,
        date_title,
        day_tracks,
        with_animation,
        key_times,
        animate_index,
    ):
        """
        max len(boxes) == 3 like douban see #7
        yield rect1, rect2, rect3
        or
        yield rect1, rect2
        or
        yield rect
        """
        if day_tracks:
            types_len = len(day_tracks)
            dom_tuple = DOM_BOX_DICT.get(types_len).get("dom")
            index = 0
            for _type in self.poster.type_list:
                num = day_tracks.get(_type)
                length_range = self.poster.length_range_by_date_dict.get(_type, 1)
                if not num:
                    continue
                dom = dom_tuple[index]
                color = self.make_color(length_range, num)
                rect = dr.rect((rect_x, rect_y), dom, fill=color)
                date_title = f"{date_title} {num} for {_type}"
                if with_animation:
                    rect = self.__add_animation(rect, key_times, animate_index)
                rect.set_desc(title=date_title)
                yield rect
                rect_y += dom_tuple[index][1]
                index += 1
        else:
            rect = dr.rect((rect_x, rect_y), DOM_BOX_TUPLE, fill=DEFAULT_DOM_COLOR)
            if with_animation:
                rect = self.__add_animation(rect, key_times, animate_index)
            yield rect

    def draw(self, dr, offset):
        if self.poster.tracks is None:
            raise BaseDrawError("No tracks to draw")
        year_size = 200 * 4.0 / 80.0
        year_style = f"font-size:{year_size}px; font-family:Arial;"
        year_length_style = f"font-size:{110 * 3.0 / 80.0}px; font-family:Arial;"
        month_names_style = "font-size:2.5px; font-family:Arial"
        total_sum_year_dict = self.poster.total_sum_year_dict
        self.poster.years.sort()
        year_count = len(self.poster.years)
        for year in range(self.poster.years[0], self.poster.years[-1] + 1)[::-1]:
            start_date_weekday, _ = calendar.monthrange(year, 1)
            github_rect_first_day = datetime.date(year, 1, 1)
            # Github profile the first day start from the last Monday of the last year
            # or the first Monday of this year.
            # It depands on if the first day of this year is Monday or not.
            github_rect_day = github_rect_first_day + datetime.timedelta(
                -start_date_weekday
            )
            year_length = total_sum_year_dict.get(year, 0)
            year_length = str(int(year_length)) + f" {self.poster.units}"
            dr.add(
                dr.text(
                    f"{year}",
                    insert=offset.tuple(),
                    fill=self.poster.colors["text"],
                    alignment_baseline="hanging",
                    style=year_style,
                )
            )

            if not self.poster.is_multiple_type:
                dr.add(
                    dr.text(
                        f"{year_length}",
                        insert=(offset.tuple()[0] + 165, offset.tuple()[1] + 5),
                        fill=self.poster.colors["text"],
                        alignment_baseline="hanging",
                        style=year_length_style,
                    )
                )
            # add month name up to the poster one by one
            # because of svg text auto trim the spaces.
            for num, name in enumerate(MONTH_NAMES):
                dr.add(
                    dr.text(
                        f"{name}",
                        insert=(offset.tuple()[0] + 15.5 * num, offset.tuple()[1] + 14),
                        fill=self.poster.colors["text"],
                        style=month_names_style,
                    )
                )

            rect_x = 10.0
            animate_index = 1
            year_count, key_times = 0, ""
            if self.poster.with_animation:
                # set default count 10
                year_count = self.poster.year_tracks_date_count_dict.get(str(year), 10)
                key_times = make_key_times(year_count)

            # add every day of this year for 53 weeks and per week has 7 days
            for _ in range(54):
                rect_y = offset.y + year_size + 2
                for _ in range(7):
                    if int(github_rect_day.year) > year:
                        break
                    rect_y += 3.5
                    date_title = str(github_rect_day)
                    day_tracks = None
                    if date_title in self.poster.tracks:
                        day_tracks = self.poster.tracks[date_title]

                        # tricky for may cause animate error
                        if animate_index < len(key_times) - 1:
                            animate_index += 1
                    gen_box_func = (
                        self._gen_day_box
                        if len(self.poster.type_list) == 1
                        else self._gen_day_boxes
                    )
                    for rect in gen_box_func(
                        dr,
                        rect_x,
                        rect_y,
                        date_title,
                        day_tracks,
                        self.poster.with_animation,
                        key_times,
                        animate_index,
                    ):
                        dr.add(rect)
                    github_rect_day += datetime.timedelta(1)
                rect_x += 3.5
            offset.y += 3.5 * 9 + year_size + 1.5

    def draw_footer(self, dr):
        text_color = self.poster.colors["text"]
        header_style = "font-size:4px; font-family:Arial"
        x = 10
        y = self.poster.height - 2.5
        index = 0
        for _type in self.poster.type_list:
            dr.add(dr.rect((x, y - 2.5), DOM_BOX_TUPLE, fill=COLOR_TUPLE[index][0]))
            dr.add(
                dr.text(
                    f": {_type}",
                    insert=(x + 3, y),
                    fill=text_color,
                    style=header_style,
                )
            )
            x += 20
            index += 1
