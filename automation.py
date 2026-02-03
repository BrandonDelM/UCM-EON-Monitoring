from aaiscloud import AaiscloudChecker
from bluesky import BlueskyChecker
from calendar_checker import CalendarChecker
from ics import ICSChecker
from listserv import ListservChecker
from news import NewsChecker
from rss import RSSChecker
from sports import SportsChecker
from youtube import YouTubeChecker
from checker import Event
import asyncio

def create_checker(source_type, source_url):
    match(source_type):
        case "aaiscloud":
            return AaiscloudChecker(source_url)
        case "bluesky":
            return BlueskyChecker(source_url)
        case "calendar":
            return CalendarChecker(source_url)
        case "ics":
            return ICSChecker(source_url)
        case "listserv":
            return ListservChecker(source_url)
        case "news":
            return NewsChecker(source_url)
        case "rss":
            return RSSChecker(source_url)
        case "sports":
            return SportsChecker(source_url)
        case "youtube":
            return YouTubeChecker(source_url)

class Automation():
    def __init__(self, checker, table):
        self.checker: AaiscloudChecker | BlueskyChecker | CalendarChecker | ICSChecker | ListservChecker | NewsChecker | RSSChecker | SportsChecker | YouTubeChecker = checker
    
    def automate(self):
        while(True):
            self.checker.check()
            events: list[Event] = self.checker.get_events()
            self.log_changes(events)
            asyncio.sleep(1800)

    def log_changes(self):
        # Clear table
        # Add all events to the postgres table
        table = "events"
        pass