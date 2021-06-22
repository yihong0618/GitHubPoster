"""Create a poster from track data."""
from collections import defaultdict

import svgwrite


class ValueRange:
    def __init__(self):
        self._lower = None
        self._upper = None

    @classmethod
    def from_pair(cls, value1, value2):
        r = cls()
        r.extend(value1)
        r.extend(value2)
        return r

    def is_valid(self):
        return self._lower is not None

    def lower(self):
        return self._lower

    def upper(self):
        return self._upper

    def diameter(self):
        if self.is_valid():
            return self.upper() - self.lower()
        return 0

    def contains(self, value):
        return self.is_valid() and (self.lower() <= value <= self.upper())

    def extend(self, value):
        if not self.is_valid():
            self._lower = value
            self._upper = value
        else:
            self._lower = min(self._lower, value)
            self._upper = max(self._upper, value)


class XY:
    """
    Represent x,y coords with properly overloaded operations.
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __mul__(self, factor):
        if isinstance(factor, XY):
            return XY(self.x * factor.x, self.y * factor.y)
        return XY(self.x * factor, self.y * factor)

    def __rmul__(self, factor):
        if isinstance(factor, XY):
            return XY(self.x * factor.x, self.y * factor.y)
        return XY(self.x * factor, self.y * factor)

    def __add__(self, other):
        return XY(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return XY(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"XY: {self.x}/{self.y}"

    def tuple(self):
        return self.x, self.y


class Poster:
    def __init__(self):
        self.title = None
        self.tracks = {}
        self.length_range = ValueRange()
        self.length_range_by_date = ValueRange()
        self.units = "metric"
        self.colors = {
            "background": "#222222",
            "text": "#FFFFFF",
            "special": "#FFFF00",
            "track": "#4DD2FF",
        }
        self.width = 200
        self.height = 300
        self.years = None
        # maybe support more type
        self.tracks_drawer = None
        self.trans = None
        self.with_animation = False
        self.animation_time = 10
        self.year_tracks_date_count_dict = defaultdict(int)

    def set_tracks(self, tracks, years):
        self.tracks = tracks
        self.years = years
        for date, num in tracks.items():
            self.year_tracks_date_count_dict[date[:4]] += 1
            self.length_range_by_date.extend(num)
        self.__compute_track_statistics()

    def set_with_animation(self, with_animation):
        self.with_animation = with_animation

    def set_animation_time(self, animation_time):
        self.animation_time = animation_time

    def draw(self, drawer, output):
        height = self.height
        width = self.width
        self.tracks_drawer = drawer
        d = svgwrite.Drawing(output, (f"{width}mm", f"{height}mm"))
        d.viewbox(0, 0, self.width, height)
        d.add(d.rect((0, 0), (width, height), fill=self.colors["background"]))
        self.__draw_header(d)
        self.__draw_tracks(d, XY(width - 20, height - 30 - 30), XY(10, 30))
        d.save()

    def __draw_tracks(self, d, size, offset):
        self.tracks_drawer.draw(d, size, offset)

    def __draw_header(self, d):
        text_color = self.colors["text"]
        title_style = "font-size:12px; font-family:Arial; font-weight:bold;"
        d.add(d.text(self.title, insert=(10, 20), fill=text_color, style=title_style))

    def __compute_track_statistics(self):
        length_range = ValueRange()
        total_sum = 0
        total_sum_year_dict = defaultdict(int)
        for date, num in self.tracks.items():
            total_sum += num
            total_sum_year_dict[int(date[:4])] += num
            length_range.extend(num)
        self.total_sum_year_dict = total_sum_year_dict
