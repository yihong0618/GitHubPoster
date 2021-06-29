"""Create a poster from track data."""
from collections import defaultdict

import svgwrite

from .structures import XY, ValueRange


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
