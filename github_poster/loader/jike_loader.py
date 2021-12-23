import json
from http.cookies import SimpleCookie
from re import compile

import pendulum
import requests

from github_poster.html_parser.jike_parse import (
    find_date_in_response,
    find_dateTime_in_html,
    find_last_id_in_html,
    find_last_id_in_response,
)
from github_poster.loader.base_loader import BaseLoader, LoadError
from github_poster.loader.config import JIKE_GRAPHQL_URL, JIKE_PERSON_URL


class JikeLoader(BaseLoader):
    track_color = "#FFE411"
    unit = "times"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.user_id = kwargs.get("user_id", "")
        self.jike_cookie = kwargs.get("jike_cookie", "")
        self.session = requests.Session()
        self.headers = {
            "authority": "web-api.okjike.com",
            "accept": "*/*",
            "dnt": "1",
            "content-type": "application/json",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "origin": "https://web.okjike.com",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--user_id",
            dest="user_id",
            type=str,
            required=False,
            help="The user id of jike",
        )
        parser.add_argument(
            "--jike_cookie",
            dest="jike_cookie",
            type=str,
            required=True,
            help="The cookie for the jike website(XHR)",
        )

    def _parse_jike_cookie(self):
        cookie = SimpleCookie()
        cookie.load(self.jike_cookie)
        cookies_dict = {}
        cookiejar = None
        for key, morsel in cookie.items():
            cookies_dict[key] = morsel.value
            cookiejar = requests.utils.cookiejar_from_dict(
                cookies_dict, cookiejar=None, overwrite=True
            )
        return cookiejar

    def _get_first_last_id(self):
        """
        get first last id for first post request
        """
        r = self.session.get(
            JIKE_PERSON_URL.format(user_id=self.user_id), headers=self.headers
        )
        if not r.ok:
            raise LoadError("Can not get first last id, please check your cookie")
        else:
            return find_last_id_in_html(r.text), find_dateTime_in_html(r.text)

    def _request_post_data(self, last_id="", resp_date_list=[]):
        """
        request next page posts
        """
        payload_data = {
            "operationName": "UserFeeds",
            "variables": {"username": "", "loadMoreKey": {"lastId": ""}},
            "query": """
            query UserFeeds($username: String!, $loadMoreKey: JSON) {
                userProfile(username: $username) {
                    username
                    feeds(loadMoreKey: $loadMoreKey) {
                    ...BasicFeedItem
                    __typename
                    }
                    __typename
                }
            }

                fragment BasicFeedItem on FeedsConnection {
                pageInfo {
                    loadMoreKey
                    hasNextPage
                    __typename
                }
                nodes {
                    ... on MessageEssential {
                    ...FeedMessageFragment
                    __typename
                    }
                    __typename
                }
                __typename
                }

                fragment FeedMessageFragment on MessageEssential {
                ...EssentialFragment
                __typename
                }

                fragment EssentialFragment on MessageEssential {
                id
                type
                createdAt
                __typename
                }
            """,
        }
        # set lastId
        payload_data["variables"]["loadMoreKey"]["lastId"] = last_id
        payload_data["variables"]["username"] = self.user_id

        r = self.session.post(
            JIKE_GRAPHQL_URL, headers=self.headers, data=json.dumps(payload_data)
        )
        resp_dates = find_date_in_response(r)
        next_last_id = find_last_id_in_response(r.text)
        resp_date_list.extend(resp_dates)
        if self._check_if_stop(resp_dates) or next_last_id == "":
            return resp_date_list
        self._request_post_data(next_last_id, resp_date_list)

    def _check_if_stop(self, list_of_dates):
        """
        stop when content other year data
        """
        r_date = compile(str(self.from_year) + ".*?")
        filter_list = list(filter(r_date.match, list_of_dates))
        return len(filter_list) != len(list_of_dates)

    def get_api_data(self):
        dateTime_cache = []
        # get first last id
        first_last_id, first_dateTime_list = self._get_first_last_id()
        if first_last_id == "":
            raise LoadError("Can not get first last id, please check your cookie")
        dateTime_cache.extend(first_dateTime_list)
        if self._check_if_stop(first_dateTime_list):
            return dateTime_cache
        else:
            # do post get more
            post_resp_dates = []
            self._request_post_data(first_last_id, post_resp_dates)
            dateTime_cache.extend(post_resp_dates)
            return dateTime_cache

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            date_str = pendulum.parse(d, tz=self.time_zone).to_date_string()
            self.number_by_date_dict[date_str] += 1
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.session.cookies = self._parse_jike_cookie()
        self.make_track_dict()
        self.make_special_number()
        print("Thanks for being addicted to jike")
        return self.number_by_date_dict, self.year_list
