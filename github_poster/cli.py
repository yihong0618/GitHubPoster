#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# some code from https://github.com/flopp/GpxTrackPoster

import argparse
import os

from github_poster.circluar_drawer import CircularDrawer
from github_poster.config import TYPE_INFO_DICT
from github_poster.drawer import Drawer
from github_poster.loader import LOADER_DICT
from github_poster.poster import Poster
from github_poster.skyline import Skyline
from github_poster.utils import parse_years

OUT_FOLDER = os.path.join(os.getcwd(), "OUT_FOLDER")


def main():
    """Handle command line arguments and call other modules as needed."""
    p = Poster()
    args_parser = argparse.ArgumentParser()
    subparser = args_parser.add_subparsers()
    for type_, loader in LOADER_DICT.items():
        parser = subparser.add_parser(name=type_)
        parser.set_defaults(type=type_, loader=loader)
        loader.add_arguments(parser)

    args = args_parser.parse_args()
    no_title_types = ("issue", "multiple")

    # we don't know issue content so use name
    p.title = (
        f"{args.me} " + TYPE_INFO_DICT.get(args.type, args.type)
        if args.type not in no_title_types
        else args.me
    )

    p.colors = {
        "background": args.background_color,
        "track": args.loader.track_color  # some type has default color
        or args.track_color,
        "special": args.special_color1,
        "special2": args.special_color2 or args.special_color,
        "text": args.text_color,
    }
    # set animate
    p.set_with_animation(args.with_animation)
    p.set_animation_time(args.animation_time)
    p.units = args.loader.unit
    from_year, to_year = parse_years(args.year)
    args_dict = dict(args._get_kwargs())
    d = LOADER_DICT.get(args.type, "duolingo")(
        from_year, to_year, args.type, **args_dict
    )
    type_list = [args.type]
    # for multiple types
    if args.type == "multiple":
        types_list = args_dict.get("types").split(",")
        # trim drop the spaces
        type_list = [t.replace(" ", "") for t in types_list]
        if args.with_skyline or args.is_circular:
            raise Exception("Skyline or Circular does not support for multiple types")
        assert len(types_list) <= 3
        for t in type_list:
            if t not in LOADER_DICT:
                raise Exception(f"{t} must in support loader types")
            d.set_loader_list(LOADER_DICT.get(t)(from_year, to_year, t, **args_dict))
    tracks, years = d.get_all_track_data()
    p.special_number = {
        "special_number1": d.special_number1,
        "special_number2": d.special_number2,
    }
    if args.special_number1:
        p.special_number["special_number1"] = args.special_number1
    if args.special_number2:
        p.special_number["special_number2"] = args.special_number2

    p.set_tracks(tracks, years, type_list)
    p.height = 35 + len(p.years) * 43
    if not os.path.exists(OUT_FOLDER):
        os.mkdir(OUT_FOLDER)
    # support different issues, maybe better way
    file_name = str(args.type)

    # make different drawer
    is_circular = args.is_circular
    d = CircularDrawer if is_circular else Drawer
    if args.type == "issue":
        issue_number = args_dict.get("issue_number", "1")
        repo_name = args_dict.get("repo_name", "").replace("/", "_")
        file_name = f"issue_{repo_name}_{issue_number}"
    if is_circular:
        file_name = f"{file_name}_circular"

        # circular type is 120*120 square
        p.height = 120
        p.width = 120

    file_name = f"{file_name}.svg"
    p.draw(d(p), os.path.join(OUT_FOLDER, file_name))

    # generate skyline
    if args.with_skyline:
        if args.skyline_year:
            year = args.skyline_year
        else:
            year = years[-1]
        # filter data
        number_by_date_dict = {k: v for k, v in tracks.items() if k[:4] == str(year)}
        skyline_name = ""
        if args.skyline_with_name:
            skyline_name = args.me
        s = Skyline(
            os.path.join(OUT_FOLDER, f"{year}_{str(args.type)}" + ".stl"),
            year,
            args.type,
            number_by_date_dict,
            skyline_name,
        )
        s.type_info_dict = TYPE_INFO_DICT
        s.make_skyline()


if __name__ == "__main__":
    main()
