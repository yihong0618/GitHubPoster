from github_poster.loader.bilibili_loader import BilibiliLoader
from github_poster.loader.cichang_loader import CiChangLoader
from github_poster.loader.dota2_loader import Dota2Loader
from github_poster.loader.duolingo_loader import DuolingoLoader
from github_poster.loader.from_github_issue_loader import GitHubIssuesLoader
from github_poster.loader.garmin_loader import GarminLoader
from github_poster.loader.github_loader import GitHubLoader
from github_poster.loader.gitlab_loader import GitLabLoader
from github_poster.loader.gpx_loader import GPXLoader
from github_poster.loader.kindle_loader import KindleLoader
from github_poster.loader.leetcode_loader import LeetcodeLoader
from github_poster.loader.multiple_loader import MutipleLoader
from github_poster.loader.nrc_loader import NRCLoader
from github_poster.loader.ns_loader import NSLoader
from github_poster.loader.shanbay_loader import ShanBayLoader
from github_poster.loader.strava_loader import StravaLoader
from github_poster.loader.twitter_loader import TwitterLoader
from github_poster.loader.wakatime_loader import WakaTimeLoader
from github_poster.loader.youtube_loader import YouTubeLoader

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
    "kindle": KindleLoader,
    "wakatime": WakaTimeLoader,
    "dota2": Dota2Loader,
    "multiple": MutipleLoader,
    "nike": NRCLoader,
    "garmin": GarminLoader,
}

__all__ = (
    "BilibiliLoader",
    "CiChangLoader",
    "Dota2Loader",
    "DuolingoLoader",
    "GitHubIssuesLoader",
    "GitHubLoader",
    "GitLabLoader",
    "GPXLoader",
    "KindleLoader",
    "LeetcodeLoader",
    "NSLoader",
    "ShanBayLoader",
    "StravaLoader",
    "TwitterLoader",
    "WakaTimeLoader",
    "YouTubeLoader",
    "MutipleLoader",
    "NRCLoader",
    "LOADER_DICT",
    "GarminLoader",
)
