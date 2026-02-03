import requests
from bs4 import BeautifulSoup

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

    def set_poster(self, poster):
        self.poster = poster
        pass

    def set_title(self, title):
        self.title = title
        pass

    def set_start(self, start):
        self.start =  start
        pass

    def set_end(self, end):
        self.end = end
        pass

    def set_building(self, building):
        self.building = building
        pass

    def set_url(self, url):
        self.url = url
        pass


class Checker():
    def __init__(self, source_url, source_type):
        self.source_url: str = source_url
        self.source_type: str = source_type
        self.events: list = []
    
    def get_soup(self, url=None, features="html.parser"):
        if url is None:
            url = self.source_url
        r = self.get_request(url)
        soup = BeautifulSoup(r.text, features=features)
        return soup

    def get_request(self, url=None):
        if url is None:
            url = self.source_url
        return requests.get(url)
    
    def get_events(self):
        return self.events