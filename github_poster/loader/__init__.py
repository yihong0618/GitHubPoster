from github_poster.loader.bbdc_loader import BBDCLoader
from github_poster.loader.bilibili_loader import BilibiliLoader
from github_poster.loader.cichang_loader import CiChangLoader
from github_poster.loader.covid_loader import CovidLoader
from github_poster.loader.dota2_loader import Dota2Loader
from github_poster.loader.duolingo_loader import DuolingoLoader
from github_poster.loader.forest_loader import ForestLoader
from github_poster.loader.from_github_issue_loader import GitHubIssuesLoader
from github_poster.loader.garmin_loader import GarminLoader
from github_poster.loader.github_loader import GitHubLoader
from github_poster.loader.gitlab_loader import GitLabLoader
from github_poster.loader.gpx_loader import GPXLoader
from github_poster.loader.jike_loader import JikeLoader
from github_poster.loader.json_loader import JsonLoader
from github_poster.loader.kindle_loader import KindleLoader
from github_poster.loader.leetcode_loader import LeetcodeLoader
from github_poster.loader.multiple_loader import MultipleLoader
from github_poster.loader.notion_loader import NotionLoader
from github_poster.loader.nrc_loader import NRCLoader
from github_poster.loader.ns_loader import NSLoader
from github_poster.loader.shanbay_loader import ShanBayLoader
from github_poster.loader.spotify_loader import SpotifyLoader
from github_poster.loader.strava_loader import StravaLoader
from github_poster.loader.summary_loader import SummaryLoader
from github_poster.loader.twitter_loader import TwitterLoader
from github_poster.loader.wakatime_loader import WakaTimeLoader
from github_poster.loader.weread_loader import WereadLoader
from github_poster.loader.youtube_loader import YouTubeLoader

LOADER_DICT = {
    "bbdc": BBDCLoader,
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
    "multiple": MultipleLoader,
    "nike": NRCLoader,
    "notion": NotionLoader,
    "garmin": GarminLoader,
    "forest": ForestLoader,
    "json": JsonLoader,
    "jike": JikeLoader,
    "summary": SummaryLoader,
    "weread": WereadLoader,
    "covid": CovidLoader,
    "spotify": SpotifyLoader,
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
    "MultipleLoader",
    "NotionLoader",
    "NRCLoader",
    "LOADER_DICT",
    "ForestLoader",
    "GarminLoader",
    "JsonLoader",
    "JikeLoader",
    "SummaryLoader",
    "BBDCLoader",
    "WereadLoader",
    "CovidLoader",
    "SpotifyLoader",
)
