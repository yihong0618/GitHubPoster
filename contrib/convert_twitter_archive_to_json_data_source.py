#!/usr/bin/env python3

"""This file converts your Twitter Archive data file into a simple JSON file like this:

{
    "2019-01-01": 123,
    "2019-01-02": 456,
    ...
}

The resulting file serves as an input file to the GitHubPoster JSON data source.

More on your Twitter Archive:
https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive

More on GitHubPoster project: https://github.com/yihong0618/GitHubPoster
"""

import argparse
import json
from collections import Counter
from datetime import datetime

# Wed Jul 08 15:04:01 +0000 2009
TIMESTAMP_FMT = "%a %b %d %H:%M:%S %z %Y"


def convert(input_file, output_file):
    with open(input_file, "r") as f:
        content = f.read()

    # Read JSON payload from the JavaScript file
    preamble = "window.YTD.tweet.part0 = "
    content = content[len(preamble) :]

    counter = Counter()
    tweets = json.loads(content)
    for tweet in tweets:
        date = str(
            datetime.strptime(tweet["tweet"]["created_at"], TIMESTAMP_FMT).date()
        )
        counter[date] += 1

    with open(output_file, "w") as f:
        json.dump(counter, f, sort_keys=True, indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "input_file", help="tweet.js file extracted from YourTwitterArchive.zip/data"
    )
    ap.add_argument(
        "output_file",
        help="path to output file, which can be fed to GitHubPoster JSON loader",
    )

    args = ap.parse_args()
    convert(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
