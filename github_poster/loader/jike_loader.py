import json
import time
from random import randint
from re import compile

import pendulum
import requests

from github_poster.html_parser.jike_parse import (
    find_count_dict_by_type_in_html,
    find_date_in_response,
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
        self.count_type = kwargs.get("count_type", "")
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
        # not more then 3 times for some day in svg are last year cells
        self.stop_time = 0

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--jike_user_id",
            dest="user_id",
            type=str,
            help="The user id of jike",
        )
        parser.add_argument(
            "--jike_cookie",
            dest="jike_cookie",
            type=str,
            required=optional,
            help="The cookie for the jike website(XHR)",
        )
        parser.add_argument(
            "--count_type",
            dest="count_type",
            type=str,
            default="record",
            choices=["record", "like", "comment", "repost", "share"],
            help="""
            The count type of jike post,
            such as 'like' or 'comment' or 'repost' or 'share'
            """,
        )

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
            return find_last_id_in_html(r.text), find_count_dict_by_type_in_html(
                r.text, self.count_type
            )

    def _request_post_data(self, last_id="", resp_data_list=None):
        """
        request next page posts
        """
        if resp_data_list is None:
            resp_data_list = []

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
                ... on OriginalPost {
                    ...LikeableFragment
                    ...CommentableFragment
                    __typename
                }
                }

                fragment EssentialFragment on MessageEssential {
                type
                shareCount
                repostCount
                createdAt
                }

                fragment LikeableFragment on LikeableMessage {
                liked
                likeCount
                __typename
                }

                fragment CommentableFragment on CommentableMessage {
                commentCount
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

        resp_data_list.extend(r.json()["data"]["userProfile"]["feeds"]["nodes"])
        if self._check_if_stop(resp_dates) or not next_last_id:
            return resp_data_list
        else:
            time.sleep(randint(1, 3))
            return self._request_post_data(next_last_id, resp_data_list)

    def _check_if_stop(self, dates):
        """
        stop when content other year data
        """
        r_date = compile(str(self.from_year) + ".*?")
        filter_list = list(filter(r_date.match, dates))
        if len(filter_list) != len(dates):
            self.stop_time += 1
        return self.stop_time == 3

    def get_api_data(self):
        data_cache = []
        # get first last id and first data
        first_last_id, first_data_dict = self._get_first_last_id()
        if not first_last_id:
            raise LoadError("Can not get first last id, please check your cookie")
        if self._check_if_stop(first_data_dict.keys()):
            return data_cache
        else:
            # do post get more
            post_resp_dates = self._request_post_data(first_last_id)
            data_cache.extend(post_resp_dates)
            return data_cache, first_data_dict

    def make_track_dict(self):
        data_list, first_data_dict = self.get_api_data()
        # add first page data
        self.number_by_date_dict.update(first_data_dict)
        # add rest page data
        count_key = self.count_type + "Count"
        for data in data_list:
            post_date = data["createdAt"]
            date_str = pendulum.parse(post_date, tz=self.time_zone).to_date_string()
            if self.count_type == "record":
                self.number_by_date_dict[date_str] += 1
            else:
                self.number_by_date_dict[date_str] += (
                    data[count_key] if data.get(count_key) else 0
                )
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.session.cookies = self.parse_cookie_string(self.jike_cookie)
        self.make_track_dict()
        self.make_special_number()
        print("Thanks for being addicted to jike.")
        return self.number_by_date_dict, self.year_list
