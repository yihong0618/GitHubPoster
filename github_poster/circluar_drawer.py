import calendar
import datetime
import math

import svgwrite
from svgwrite import animate

from github_poster.drawer import Drawer
from github_poster.err import CircularDrawError
from github_poster.structures import XY, ValueRange
from github_poster.utils import make_key_times


class CircularDrawer(Drawer):

    # somecode from https://github.com/flopp/GpxTrackPoster
    name = "circular"

    def __init__(self, p):
        super().__init__(p)

    def draw(self, dr, size):
        if self.poster.tracks is None:
            raise CircularDrawError("No tracks to draw.")
        if self.poster.length_range_by_date is None:
            return
        margin = XY(10, 10)
        key_times = make_key_times(len(self.poster.years))
        animate_index = 1
        for year in range(self.poster.years[0], self.poster.years[-1] + 1):
            values = ["0"] * len(key_times)
            values[animate_index] = "1"
            values_str = ";".join(values)
            key_animate = self._make_key_anmiate(values_str, key_times)
            self._draw_year(dr, size, margin, year, key_animate)
            animate_index += 1

    def _draw_year(self, dr, size, offset, year, key_animate):
        min_size = min(size.x, size.y)
        outer_radius = 0.5 * min_size - 6
        radius_range = ValueRange.from_pair(outer_radius / 4, outer_radius)
        center = offset + 0.5 * size

        year_style = f"dominant-baseline: central; font-size:{min_size * 4.0 / 80.0}px; \
                       font-family:Arial;"
        month_style = f"font-size:{min_size * 3.0 / 80.0}px; font-family:Arial;"

        year_text = dr.text(
            f"{year}",
            insert=(center.x, center.y),
            fill=self.poster.colors["text"],
            text_anchor="middle",
            alignment_baseline="middle",
            style=year_style,
        )
        year_text.add(key_animate)
        dr.add(year_text)

        year_length = self.poster.total_sum_year_dict.get(year, 0)
        year_length_str = str(int(year_length)) + f" {self.poster.units}"

        year_stats = dr.text(
            year_length_str,
            insert=(115 - len(str(year_length_str)), 8),  # TODO: make this dynamic
            fill=self.poster.colors["text"],
            text_anchor="middle",
            alignment_baseline="middle",
            style=year_style,
        )
        year_stats.add(key_animate)
        dr.add(year_stats)

        # user stats
        user_stats = dr.text(
            f"{self.poster.title}",
            insert=(5 + len(self.poster.title), 8),  # ToDO: make this dynamic
            fill=self.poster.colors["text"],
            text_anchor="middle",
            alignment_baseline="middle",
            style=year_style,
        )
        user_stats.add(key_animate)
        dr.add(user_stats)
        df = 360.0 / (366 if calendar.isleap(year) else 365)
        day = 0
        date = datetime.date(year, 1, 1)
        while date.year == year:
            text_date = date.strftime("%Y-%m-%d")
            a1 = math.radians(day * df)
            a2 = math.radians((day + 1) * df)
            if date.day == 1:
                (_, last_day) = calendar.monthrange(date.year, date.month)
                a3 = math.radians((day + last_day - 1) * df)
                sin_a1, cos_a1 = math.sin(a1), math.cos(a1)
                sin_a3, cos_a3 = math.sin(a3), math.cos(a3)
                r1 = outer_radius + 1
                r2 = outer_radius + 6
                r3 = outer_radius + 2
                line = dr.line(
                    start=(center + r1 * XY(sin_a1, -cos_a1)).tuple(),
                    end=(center + r2 * XY(sin_a1, -cos_a1)).tuple(),
                    stroke=self.poster.colors["text"],
                    stroke_width=0.3,
                )
                line.add(key_animate)
                dr.add(line)
                path = dr.path(
                    d=("M", center.x + r3 * sin_a1, center.y - r3 * cos_a1),
                    fill="none",
                    stroke="none",
                )
                path.push(
                    f"a{r3},{r3} 0 0,1 {r3 * (sin_a3 - sin_a1)}, \
                    {r3 * (cos_a1 - cos_a3)}"
                )
                path.add(key_animate)
                dr.add(path)
                tpath = svgwrite.text.TextPath(
                    path, date.strftime("%B"), startOffset=(0.5 * r3 * (a3 - a1))
                )
                text = dr.text(
                    "",
                    fill=self.poster.colors["text"],
                    text_anchor="middle",
                    style=month_style,
                )
                text.add(tpath)
                text.add(key_animate)
                dr.add(text)

            if text_date in self.poster.tracks:
                self._draw_circle_segment(
                    dr,
                    self.poster.tracks[text_date],
                    a1,
                    a2,
                    radius_range,
                    center,
                    key_animate,
                )
            day += 1
            date += datetime.timedelta(1)

    def _make_key_anmiate(self, values, key_times):
        dur = len(key_times)
        return animate.Animate(
            "opacity",
            dur=f"{dur}s",
            values=values,
            keyTimes=";".join(key_times),
            repeatCount="indefinite",
        )

    def _draw_circle_segment(
        self,
        dr,
        length,
        a1,
        a2,
        rr,
        center,
        key_animate,
    ):
        color = self.make_color(self.poster.length_range_by_date, length)
        color = self.make_color(self.poster.length_range_by_date, length)
        r1 = rr.lower()
        r2 = (
            rr.lower()
            + rr.diameter() * length / self.poster.length_range_by_date.upper()
        )
        sin_a1, cos_a1 = math.sin(a1), math.cos(a1)
        sin_a2, cos_a2 = math.sin(a2), math.cos(a2)
        path = dr.path(
            d=("M", center.x + r1 * sin_a1, center.y - r1 * cos_a1),
            fill=color,
            stroke="none",
        )
        path.push("l", (r2 - r1) * sin_a1, (r1 - r2) * cos_a1)
        path.push(f"a{r2},{r2} 0 0,0 {r2 * (sin_a2 - sin_a1)},{r2 * (cos_a1 - cos_a2)}")
        path.push("l", (r1 - r2) * sin_a2, (r2 - r1) * cos_a2)
        path.add(key_animate)
        dr.add(path)
