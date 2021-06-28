import re
from itertools import count as itercount
from itertools import takewhile

import colour


def interpolate_color(color1, color2, ratio):
    if ratio < 0:
        ratio = 0
    elif ratio > 1:
        ratio = 1
    c1 = colour.Color(color1)
    c2 = colour.Color(color2)
    c3 = colour.Color(
        hue=((1 - ratio) * c1.hue + ratio * c2.hue),
        saturation=((1 - ratio) * c1.saturation + ratio * c2.saturation),
        luminance=((1 - ratio) * c1.luminance + ratio * c2.luminance),
    )
    return c3.hex_l


def parse_years(s):
    """Parse a plaintext range of years into a pair of years

    Attempt to turn the input string into a pair of year values, from_year and to_year.
    If one year is passed, both from_year and to_year will be set to that year.
    If a range like '2016-2018' is passed, from_year will be set to 2016,
    and to_year will be set to 2018.

    Args:
        s: A string representing a range of years or a single year
    """
    m = re.match(r"^\d+$", s)
    if m:
        from_year = int(s)
        to_year = from_year
        return from_year, to_year
    m = re.match(r"^(\d+)-(\d+)$", s)
    if m:
        y1, y2 = int(m.group(1)), int(m.group(2))
        if y1 <= y2:
            from_year = y1
            to_year = y2
        else:
            from_year = y2
            to_year = y1
    return from_year, to_year


def make_key_times(year_count):
    """
    year_count: year run date count
    return: list of key times points
    should append `1` because the svg keyTimes rule
    """
    s = list(takewhile(lambda n: n < 1, itercount(0, 1 / year_count)))
    s.append(1)
    return [str(round(i, 2)) for i in s]
