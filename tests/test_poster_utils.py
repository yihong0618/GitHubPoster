from github_poster.utils import interpolate_color, make_key_times, parse_years


def test_interpolate_color():
    assert interpolate_color("#000000", "#ffffff", 0) == "#000000"
    assert interpolate_color("#000000", "#ffffff", 1) == "#ffffff"
    assert interpolate_color("#000000", "#ffffff", 0.5) == "#7f7f7f"
    assert interpolate_color("#000000", "#ffffff", -100) == "#000000"
    assert interpolate_color("#000000", "#ffffff", 12345) == "#ffffff"


def test_parse_years():
    assert parse_years("2012") == (2012, 2012)
    assert parse_years("2015-2021") == (2015, 2021)
    assert parse_years("2021-2015") == (2015, 2021)


def test_make_key_times():
    assert make_key_times(5) == ["0", "0.2", "0.4", "0.6", "0.8", "1"]
