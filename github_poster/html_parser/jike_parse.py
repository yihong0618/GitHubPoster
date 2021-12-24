import json
from re import findall


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


def find_date_in_response(r):
    date_list = []
    for item in r.json()["data"]["userProfile"]["feeds"]["nodes"]:
        date_list.append(item["createdAt"])
    return date_list
