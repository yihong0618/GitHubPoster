import calendar
import datetime
import svgwrite

from .utils import interpolate_color
from .poster import Poster


class Drawer:
    def __init__(self, p):
        self.poster = p

    def color(self, length_range, length, is_special):
        color1 = (
            self.poster.colors["special"] if is_special else self.poster.colors["track"]
        )
        color2 = (
            self.poster.colors["special2"]
            if is_special
            else self.poster.colors["track2"]
        )

        diff = length_range.diameter()
        if diff == 0:
            return color1

        return interpolate_color(color1, color2, (length - length_range.lower()) / diff)

    def draw(self, dr, size, offset):
        if self.poster.tracks is None:
            raise Exception("No tracks to draw")
        year_size = 200 * 4.0 / 80.0
        year_style = f"font-size:{year_size}px; font-family:Arial;"
        year_length_style = f"font-size:{110 * 3.0 / 80.0}px; font-family:Arial;"
        month_names_style = f"font-size:2.5px; font-family:Arial"
        total_sum_year_dict = self.poster.total_sum_year_dict
        self.poster.years.sort()
        for year in range(self.poster.years[0], self.poster.years[-1] + 1)[::-1]:
            start_date_weekday, _ = calendar.monthrange(year, 1)
            github_rect_first_day = datetime.date(year, 1, 1)
            # Github profile the first day start from the last Monday of the last year or the first Monday of this year
            # It depands on if the first day of this year is Monday or not.
            github_rect_day = github_rect_first_day + datetime.timedelta(
                -start_date_weekday
            )
            year_length = total_sum_year_dict.get(year, 0)
            year_length = str(year_length) + f" {self.poster.units}"
            month_names = [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]
            dr.add(
                dr.text(
                    f"{year}",
                    insert=offset.tuple(),
                    fill=self.poster.colors["text"],
                    alignment_baseline="hanging",
                    style=year_style,
                )
            )

            dr.add(
                dr.text(
                    f"{year_length}",
                    insert=(offset.tuple()[0] + 165, offset.tuple()[1] + 2),
                    fill=self.poster.colors["text"],
                    alignment_baseline="hanging",
                    style=year_length_style,
                )
            )
            # add month name up to the poster one by one because of svg text auto trim the spaces.
            for num, name in enumerate(month_names):
                dr.add(
                    dr.text(
                        f"{name}",
                        insert=(offset.tuple()[0] + 15.5 * num, offset.tuple()[1] + 14),
                        fill=self.poster.colors["text"],
                        style=month_names_style,
                    )
                )

            rect_x = 10.0
            dom = (2.6, 2.6)
            # add every day of this year for 53 weeks and per week has 7 days
            for i in range(54):
                rect_y = offset.y + year_size + 2
                for j in range(7):
                    if int(github_rect_day.year) > year:
                        break
                    rect_y += 3.5
                    color = "#444444"
                    date_title = str(github_rect_day)
                    if date_title in self.poster.tracks:
                        num = self.poster.tracks[date_title]
                        special_num1 = self.poster.special_number["special_number1"]
                        special_num2 = self.poster.special_number["special_number2"]
                        has_special = special_num2 < num < special_num1

                        color = self.color(
                            self.poster.length_range_by_date, num, has_special
                        )
                        if num >= special_num1:
                            color = self.poster.colors.get(
                                "special2"
                            ) or self.poster.colors.get("special")
                        date_title = f"{date_title} {num} {self.poster.units}"
                    rect = dr.rect((rect_x, rect_y), dom, fill=color)
                    rect.set_desc(title=date_title)
                    dr.add(rect)
                    github_rect_day += datetime.timedelta(1)
                rect_x += 3.5
            offset.y += 3.5 * 9 + year_size + 1.5
