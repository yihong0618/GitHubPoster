from collections import namedtuple

# China timezone if you are from others please change this
TIME_ZONE = "Asia/Shanghai"

# shanbay -- no need to login
SHANBAY_CALENDAR_API = (
    "https://apiv3.shanbay.com/uc/checkin/calendar/dates/"
    "?user_id={user_name}&start_date={start_date}&end_date={end_date}"
)

# duolingo -- no need to login
DUOLINGO_CALENDAR_API = (
    "https://www.duolingo.com/2017-06-30/users/{user_id}/xp_summaries"
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

# GitHub for furture use
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
