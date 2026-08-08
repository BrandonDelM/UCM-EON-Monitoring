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
from database import *

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

CHECKER = AaiscloudChecker | BlueskyChecker | CalendarChecker | ICSChecker | ListservChecker | NewsChecker | RSSChecker | SportsChecker | YouTubeChecker

class Automation():
    def __init__(self, checker):
        self.checker: CHECKER = checker
    
    async def automate(self):
        while(True):
            print(f"Checking {self.checker.source_type} {self.checker.source_url}")
            try:
                self.checker.clear_events()
                await self.checker.check()
                if self.checker.get_events():
                    self.log_changes()
            except Exception as e:
                print(f"Exception while logging {self.checker.source_url}: {e}")
            await asyncio.sleep(1800)

    def log_changes(self):
        # Clear table for the new events
        delete_specific_rows(self.checker.get_source_url())
        # Add the rows to database
        add_to_database(self.checker.get_events(), self.checker.get_source_url(), self.checker.get_source_type())