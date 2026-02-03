import requests
from bs4 import BeautifulSoup
import httpx

class Event():
    def __init__(self, source_url, source_type, poster=None, title=None, start=None, end=None, building=None, url=None):
        self.source_url: str = source_url
        self.source_type: str = source_type
        self.poster: str | None = poster
        self.title: str | None = title
        self.start: str | None = start
        self.end: str | None = end
        self.building: str | None = building
        self.url: str | None = url

    def get_poster(self):
        return self.poster
    
    def get_title(self):
        return self.title
    
    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end
    
    def get_building(self):
        return self.building
    
    def get_url(self):
        return self.url

    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        return (self.poster == other.poster and
                self.title == other.title and
                self.start == other.start and
                self.end == other.end and
                self.building == other.building and
                self.url == other.url)


class Checker():
    def __init__(self, source_url, source_type):
        self.source_url: str = source_url
        self.source_type: str = source_type
        self.events: list[Event] = []
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def get_soup(self, url: str | None = None, features: str ="html.parser"):
        if url is None:
            url = self.source_url
        r = await self.get_request(url=url)
        if r is None:
            return None
        soup = BeautifulSoup(r.text, features=features)
        return soup

    async def get_request(self, url: str | None = None, headers: str | None = None):
        try:
            if url is None:
                url = self.source_url
            return await self.client.get(url=url, headers=headers)
        except Exception as e:
            print(f"Couldn't get the request for {url}")
            return None
    
    def get_events(self):
        return self.events
    
    def clear_events(self):
        self.events = []

    def get_source_type(self):
        return self.source_type

    def get_source_url(self):
        return self.source_url