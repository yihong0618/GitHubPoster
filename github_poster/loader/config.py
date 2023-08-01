from collections import namedtuple

# China timezone if you are from others please change this
TIME_ZONE = "Asia/Shanghai"

# neodb -- need to get token from https://neodb.social/developer/
NEODB_API = "https://neodb.social/api/me/shelf/{type}?page={page}"

# shanbay -- no need to login
SHANBAY_WORD_API = (
    "https://apiv3.shanbay.com/uc/checkin/logs?user_id={user_name}&ipp=20&page={page}"
)

# duolingo -- no need to login
DUOLINGO_CALENDAR_API = (
    "https://ios-api-2.duolingo.com/2017-06-30/users/{user_id}/xp_summaries"
    "?endDate={end_date}&startDate={start_date}&timezone=Asia/Shanghai"
)

# cichang -- need to login
HJ_APPKEY = "45fd17e02003d89bee7f046bb494de13"
CICHANG_LOGIN_URL = (
    "https://pass.hujiang.com/Handler/UCenter.json?action=Login&isapp=true"
    "&language=zh_CN&password={password}&timezone=8&user_domain=hj&username={user_name}"
)
CICHANG_COVERT_URL = "https://pass-cdn.hjapi.com/v1.1/access_token/convert"
CICHANG_CLAENDAR_URL = (
    "https://cichang.hjapi.com/v3/user/center/"
    "?userId={user_id}&startDate={start_date}&endDate={end_date}"
)

# switch -- need to packet sniffer (to get device id and token)
TOKEN_API_URL = "https://accounts.nintendo.com/connect/1.0.0/api/token"
NS_CLIENT_ID = "54789befb391a838"
NS_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:jwt-bearer-session-token"
NS_TOKEN_URL = "https://accounts.nintendo.com/connect/1.0.0/api/token"
NS_CLAENDAR_URL = (
    "https://api-lp1.pctl.srv.nintendo.net/moon/v1/devices"
    "/{device_id}/monthly_summaries/{month}"
)

# gpx need a gpx folder
GPX_ACTIVITY_NAME_TUPLE = namedtuple("activity", "date distance")

# GitHub for future use
GITHUB_BASE_URL = "https://github.com"

# LeetCode
LEETCODE_SUBMISSIONS_URL = (
    "https://leetcode.com/api/submissions/?offset={offset}&limit=20&lastkey={last_key}"
)
LEETCODE_CN_SUBMISSIONS_URL = (
    "https://leetcode-cn.com/api/submissions/"
    "?offset={offset}&limit=20&lastkey={last_key}"
)

# Bilibili
BILIBILI_HISTORY_URL = (
    "https://api.bilibili.com/x/web-interface/history/cursor"
    "?max={max_oid}&view_at={view_at}&business=archive"
)

# GitHub
GITHUB_CONTRIBUCTIONS_URL = (
    "https://github.com/users/{user_name}/contributions?from={start_day}&to={end_day}"
)

# GitLab
GITLAB_LATEST_URL = "{gitlab_base_url}/users/{user_name}/calendar.json"
GITLAB_ONE_DAY_URL = (
    "{gitlab_base_url}/users/{user_name}/calendar_activities?date={date_str}"
)

# Kindle
KINDLE_HISTORY_URL = "https://www.amazon.com/kindle/reading/insights"
KINDLE_CN_HISTORY_URL = "https://www.amazon.cn/kindle/reading/insights"
KINDLE_HEADER = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/1AE148",
}

# WakaTime
WAKATIME_SUMMARY_URL = (
    "https://wakatime.com/api/v1/users/current/summaries"
    "?api_key={wakatime_key}&start={from_year}&end={to_year}"
)

# Dota2
DOTA2_CALENDAR_API = "https://api.opendota.com/api/players/{dota2_id}/matches"

# NRC (nike)
NIKE_TOKEN_REFRESH_URL = "https://unite.nike.com/tokenRefresh"
NIKE_CLIENT_ID = "HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH"
NIKE_BASE_URL = "https://api.nike.com/sport/v3/me"

# forest(need to login)
FOREST_URL_HEAD = "https://forest.dc.upwardsware.com"
FOREST_CN_URL_HEAD = "https://forest-china.upwardsware.com"
FOREST_LOGIN_URL = FOREST_URL_HEAD + "/api/v1/sessions"
FOREST_CLAENDAR_URL = (
    FOREST_URL_HEAD
    + "/api/v1/plants/updated_plants?update_since={date}&seekruid={user_id}"
)
FOREST_CN_LOGIN_URL = FOREST_CN_URL_HEAD + "/api/v1/sessions"
FOREST_CN_CLAENDAR_URL = (
    FOREST_CN_URL_HEAD
    + "/api/v1/plants/updated_plants?update_since={date}&seekruid={user_id}"
)

# jike
JIKE_GRAPHQL_URL = "https://web-api.okjike.com/api/graphql"
JIKE_PERSON_URL = "https://web.okjike.com/u/{user_id}"

# bbdc
BBDC_API_URL = "https://learnywhere.cn/bb/dashboard/profile/search?userId={user_id}"

# Notion
NOTION_API_URL = "https://api.notion.com/v1/databases/{database_id}/query"
NOTION_API_VERSION = "2021-08-16"

# Weread
WEREAD_BASE_URL = "https://weread.qq.com/"
WEREAD_HISTORY_URL = (
    "https://i.weread.qq.com/readdetail?baseTimestamp=0&count=32&type=1"
)

# COVID
COVID_API = "https://pomber.github.io/covid19/timeseries.json"

OPEN_LANGUAGE_LOGIN_URL = (
    "https://api.openlanguage.com/passport/user/login/?"
    "version_code=8.2.3&app_name=open_language"
    "&vendor_id=5E43BCDC-D306-47C0-86D0-3248D4B77267"
    "&device_id=884423380449783&channel=App%20Store"
    "&mix_mode=1&multi_login=1&resolution=828%2A1792"
    "&aid=1335&app_id=1335&install_id=180755913509454"
    "&update_version_code=82300&ac=WIFI&os_version=16.0.2"
    "&timezone=Asia%2FShanghai&ez_version=85&ssmix=a"
    "&timezone_offset=28800000&device_platform=iphone"
    "&iid=180755913509454&ab_client=a1%2Cf2%2Cf7%2Ce1"
    "&device_type=iPhone11%2C8"
)

OPEN_LANGUAGE_X_LADON = "FMByTcspdXr0+Zu4p2x0j9698vNGIgJr2+7Y0hqdGnNW94US"

OPEN_LANGUAGE_X_ARGUS = (
    "uoviDe0vjDP7TP1eJ5GR1Iv3z0yZOjjZvO81C+Niy5FgO8ghZueIU"
    "/yNG/ooGjfWjNZs2XBRSS/PIXsm8IZYKczptvpD2VoUajNVMGxWMv"
    "PbygEzVtgvVCphnR+A7VNZQYNU217125E25PwuBFqx8j43qB/H29+u"
    "P0h1FmNHePHDMB+FwHeeawWE9X2aT5zcZ2O/65deSknksNXFFCLGgp"
    "H7u3HSfFj6hW2M+NRfda2JYOCU2N/eheYxXoZXmhnVfLE="
)

OPEN_LANGUAGE_RECORD_URL = (
    "https://api.openlanguage.com/ez/studentapp/v15/clockInRecord"
    "?start_date={start_date}&end_date={end_date}"
)

OPEN_LANGUAGE_ACCOUNT_PASSWORD_DICT = {
    "0": "35",
    "1": "34",
    "2": "37",
    "3": "36",
    "4": "31",
    "5": "30",
    "6": "33",
    "7": "32",
    "8": "3d",
    "9": "3c",
    "a": "64",
    "b": "67",
    "c": "66",
    "d": "61",
    "e": "60",
    "f": "63",
    "g": "62",
    "h": "6d",
    "i": "6c",
    "j": "6f",
    "k": "6e",
    "l": "69",
    "m": "68",
    "n": "6b",
    "o": "6a",
    "p": "75",
    "q": "74",
    "r": "77",
    "s": "76",
    "t": "71",
    "u": "70",
    "v": "73",
    "w": "72",
    "x": "7d",
    "y": "7c",
    "z": "7f",
    "A": "44",
    "B": "47",
    "C": "46",
    "D": "41",
    "E": "40",
    "F": "43",
    "G": "42",
    "H": "4d",
    "I": "4c",
    "J": "4f",
    "K": "4e",
    "L": "49",
    "M": "48",
    "N": "4b",
    "O": "4a",
    "P": "55",
    "Q": "54",
    "R": "57",
    "S": "56",
    "T": "51",
    "U": "50",
    "V": "53",
    "W": "52",
    "X": "5d",
    "Y": "5c",
    "Z": "5f",
}
