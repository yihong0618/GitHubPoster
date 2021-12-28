import json
from collections import defaultdict
from re import compile, findall

import pendulum

from github_poster.loader.config import TIME_ZONE


def find_last_id_in_response(text):
    """
    get last id from response
    """
    json_data = json.loads(text)
    load_more_key = json_data["data"]["userProfile"]["feeds"]["pageInfo"]["loadMoreKey"]
    return "" if load_more_key is None else load_more_key["lastId"]


def find_last_id_in_html(text):
    """
    find last id in html
    "json":{"lastId":"xxx"}}
    """
    r = findall('"json":{"lastId":"(.*?)"}', text)
    return r[0] if r else ""


def find_dateTime_in_html(text):
    """
    find dateTime in html
    """
    r = findall('<time dateTime="(.*?)">', text)
    if r:
        return r
    return []


def find_count_dict_by_type_in_html(text, count_type):
    """
    find count by type in html:
    likeCount, commentCount, shareCount, repostCount, recordCount
    """
    number_by_date_dict = defaultdict(int)
    # find all post data
    posts = findall('"__typename".*?"readTrackInfo"', text)
    if posts:
        r_count = compile(count_type + "Count.*?(\\d+)")
        create_at = compile('"createdAt":"(.*?)"')
        for post in posts:
            # find count by type
            date = create_at.findall(post)[0]
            if date:
                date_str = pendulum.parse(date, tz=TIME_ZONE).to_date_string()
                if count_type == "record":
                    count = 1
                else:
                    count = r_count.findall(post)[0]
                number_by_date_dict[date_str] += int(count)
    return number_by_date_dict


def find_date_in_response(r):
    date_list = []
    for item in r.json()["data"]["userProfile"]["feeds"]["nodes"]:
        date_list.append(item["createdAt"])
    return date_list
