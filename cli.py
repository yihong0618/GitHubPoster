#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# some code from https://github.com/flopp/GpxTrackPoster

import argparse
import os
from datetime import datetime

from github_poster import poster, drawer
from github_poster.utils import parse_years
from loader import (
    DuolingoLoader,
    ShanBayLoader,
    StravaLoader,
    CiChangLoader,
    NSLoader,
    GPXLoader,
    GitHubIssuesLoader,
    LeetcodeLoader,
    TwitterLoader,
    YouTubeLoader,
    BilibiliLoader,
    GitHubLoader,
    GitLabLoader,
)
from skyline import Skyline

LOADER_DICT = {
    "duolingo": DuolingoLoader,
    "shanbay": ShanBayLoader,
    "strava": StravaLoader,
    "cichang": CiChangLoader,
    "ns": NSLoader,
    "gpx": GPXLoader,
    "issue": GitHubIssuesLoader,
    "leetcode": LeetcodeLoader,
    "twitter": TwitterLoader,
    "youtube": YouTubeLoader,
    "bilibili": BilibiliLoader,
    "github": GitHubLoader,
    "gitlab": GitLabLoader,
}

# TODO refactor
UNIT_DICT = {
    "duolingo": "XP",
    "shanbay": "days",
    "strava": "km",
    "gpx": "km",
    "cichang": "words",
    "ns": "mins",
    "issue": "times",
    "leetcode": "subs",
    "twitter": "tweets",
    "youtube": "videos",
    "bilibili": "videos",
    "github": "cons",
    "gitlab": "cons",
}

## default color for different type
## add more default dict here
TRACK_COLOR_DICT = {
    "shanbay": "#33C6A4",
    "twitter": "#1C9CEA",
    "youtube": "#FFFFFF",
    "bilibili": "#FB7299",
    "github": "#9BE9A8",
    "gitlab": "#ACD5F2",
}

TYPES = '", "'.join(LOADER_DICT.keys())

OUT_FOLDER = os.path.join(os.getcwd(), "OUT_FOLDER")


def main():
    """Handle command line arguments and call other modules as needed."""
    p = poster.Poster()
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--type",
        metavar="TYPE",
        default="duolingo",
        choices=LOADER_DICT.keys(),
        help=f'Type of poster to create (default: "duolingo", available: "{TYPES}").',
    )
    args_parser.add_argument(
        "--gpx-dir",
        dest="gpx_dir",
        metavar="DIR",
        type=str,
        default="GPX_FOLDER",
        help="Directory containing GPX files",
    )
    args_parser.add_argument(
        "--year",
        metavar="YEAR",
        type=str,
        default=str(datetime.now().year),
        help='Filter tracks by year; "NUM", "NUM-NUM", "all" (default: all years)',
    )
    args_parser.add_argument(
        "--me",
        metavar="NAME",
        type=str,
        default="Joey",
        help='Athlete name to display (default: "Joey").',
    )
    args_parser.add_argument(
        "--background-color",
        dest="background_color",
        metavar="COLOR",
        type=str,
        default="#222222",
        help='Background color of poster (default: "#222222").',
    )
    args_parser.add_argument(
        "--track-color",
        dest="track_color",
        metavar="COLOR",
        type=str,
        default="#4DD2FF",
        help='Color of tracks (default: "#4DD2FF").',
    )
    args_parser.add_argument(
        "--text-color",
        dest="text_color",
        metavar="COLOR",
        type=str,
        default="#FFFFFF",
        help='Color of text (default: "#FFFFFF").',
    )
    args_parser.add_argument(
        "--special-color1",
        dest="special_color1",
        metavar="COLOR",
        default="yellow",
        help='Special track color (default: "yellow").',
    )
    args_parser.add_argument(
        "--special-color2",
        dest="special_color2",
        metavar="COLOR",
        default="red",
        help="Secondary color of special tracks (default: red).",
    )
    args_parser.add_argument(
        "--special-number1",
        dest="special_number1",
        type=float,
        default=0,
        help="Special number 1",
    )
    args_parser.add_argument(
        "--special-number2",
        dest="special_number2",
        type=float,
        default=0,
        help="Special number 2",
    )
    args_parser.add_argument(
        "--with-animation",
        dest="with_animation",
        action="store_true",
        help="add animation to the poster",
    )
    args_parser.add_argument(
        "--animation-time",
        dest="animation_time",
        type=int,
        default=10,
        help="animation duration (default: 10s)",
    )
    # skyline args here
    args_parser.add_argument(
        "--with-skyline",
        dest="with_skyline",
        action="store_true",
        help="with skyline(stl file)",
    )

    args_parser.add_argument(
        "--skyline-year",
        dest="skyline_year",
        type=str,
        default="",
        help="the year to generate skyline",
    )

    # strava
    args_parser.add_argument(
        "--strava_client_id",
        dest="strava_client_id",
        type=str,
        default="",
        help="",
    )
    args_parser.add_argument(
        "--strava_client_secret",
        dest="strava_client_secret",
        type=str,
        default="",
        help="",
    )
    args_parser.add_argument(
        "--strava_refresh_token",
        dest="strava_refresh_token",
        type=str,
        default="",
        help="",
    )
    # duolingo
    args_parser.add_argument(
        "--duolingo_user_name",
        dest="duolingo_user_name",
        type=str,
        default="",
        help="",
    )
    # shanbay
    args_parser.add_argument(
        "--shanbay_user_name",
        dest="shanbay_user_name",
        type=str,
        default="",
        help="",
    )

    # cichang
    args_parser.add_argument(
        "--cichang_user_name",
        dest="cichang_user_name",
        type=str,
        default="",
        help="",
    )
    args_parser.add_argument(
        "--cichang_password",
        dest="cichang_password",
        type=str,
        default="",
        help="",
    )

    # nintendo setting
    args_parser.add_argument(
        "--ns_device_id",
        dest="ns_device_id",
        type=str,
        default="",
        help="",
    )
    args_parser.add_argument(
        "--ns_smart_device_id",
        dest="ns_smart_device_id",
        type=str,
        default="",
        help="",
    )
    args_parser.add_argument(
        "--ns_session_token",
        dest="ns_session_token",
        type=str,
        default="",
        help="",
    )

    # GitHub issue args
    args_parser.add_argument(
        "--github_issue_number",
        dest="github_issue_number",
        type=str,
        default="",
        help="",
    )
    args_parser.add_argument(
        "--github_repo_name",
        dest="github_repo_name",
        type=str,
        default="",
        help="",
    )
    args_parser.add_argument(
        "--github_token",
        dest="github_token",
        type=str,
        default="",
        help="",
    )
    # LeetCode
    args_parser.add_argument(
        "--leetcode_cookie",
        dest="leetcode_cookie",
        type=str,
        default="",
        help="",
    )
    args_parser.add_argument(
        "--is-cn",
        dest="is_cn",
        action="store_true",
        help="if leetcode accout is com",
    )
    # twitter
    args_parser.add_argument(
        "--twitter_user_name",
        dest="twitter_user_name",
        type=str,
        default="",
        help="",
    )
    # YouTube
    args_parser.add_argument(
        "--input-dir",
        dest="input_dir",
        metavar="DIR",
        type=str,
        default="IN_FOLDER",
        help="Directory containing input files.",
    )
    args_parser.add_argument(
        "--youtube-file",
        dest="youtube_file",
        type=str,
        default="watch-history.json",
        help="Deafault youtube history file",
    )
    # Bilibili
    args_parser.add_argument(
        "--bilibili_cookie",
        dest="bilibili_cookie",
        type=str,
        default="",
        help="",
    )
    # GitHub Contributions
    args_parser.add_argument(
        "--github_user_name",
        dest="github_user_name",
        type=str,
        default="",
        help="",
    )
    # GitLab Contributions
    args_parser.add_argument(
        "--gitlab_user_name",
        dest="gitlab_user_name",
        type=str,
        default="",
        help="",
    )

    args = args_parser.parse_args()

    # we don't know issue content so use name
    p.title = (
        f"{args.me} " + str(args.type).upper() if args.type != "issue" else args.me
    )

    p.colors = {
        "background": args.background_color,
        "track": TRACK_COLOR_DICT.get(args.type)
        or args.track_color,  # some type has default color
        "special": args.special_color1,
        "special2": args.special_color2 or args.special_color,
        "text": args.text_color,
    }
    # set animate
    p.set_with_animation(args.with_animation)
    p.set_animation_time(args.animation_time)
    p.units = UNIT_DICT.get(args.type, "times")
    from_year, to_year = parse_years(args.year)
    d = LOADER_DICT.get(args.type, "duolingo")(
        from_year, to_year, **dict(args._get_kwargs())
    )
    tracks, years = d.get_all_track_data()
    p.special_number = {
        "special_number1": d.special_number1,
        "special_number2": d.special_number2,
    }
    if args.special_number1:
        p.special_number["special_number1"] = args.special_number1
    if args.special_number2:
        p.special_number["special_number2"] = args.special_number2
    p.set_tracks(tracks, years)
    p.height = 35 + len(p.years) * 43
    if not os.path.exists(OUT_FOLDER):
        os.mkdir(OUT_FOLDER)
    p.draw(drawer.Drawer(p), os.path.join(OUT_FOLDER, str(args.type) + ".svg"))

    # generate skyline
    if args.with_skyline:
        if args.skyline_year:
            year = args.skyline_year
        else:
            year = years[-1]
        # filter data
        number_by_date_dict = {k: v for k, v in tracks.items() if k[:4] == str(year)}
        s = Skyline(os.path.join(OUT_FOLDER, f"{year}_{str(args.type)}" + ".stl"), year, args.type, number_by_date_dict)
        s.make_skyline()


if __name__ == "__main__":
    main()
