import requests
from bs4 import BeautifulSoup

class Event():
    def __init__(self, source_url, source_type, poster="", title="", start="", end="", building="", url=""):
        self.source_url: str = source_url
        self.source_type: str = source_type
        self.poster: str = poster
        self.title: str = title
        self.start: str = start
        self.end: str = end
        self.building: str = building
        self.url: str = url

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
    
    def get_soup(self, features="html.parser"):
        r = requests.get(self.source_url)
        soup = BeautifulSoup(r.text, features=features)
        return soup
    
    def find_class(self, soup, check):
        if soup.find(class_=check):
            return soup.find(class_=check)
        return None

    def find(self, soup, check):
        if soup.find(check):
            return soup.find(check)
        return None
        
    def find_all(self, soup, check):
        if soup.find_all(check):
            return soup.find_all(check)
        return None

class CalendarChecker(Checker):
    def __init__(self, source_url, source_type):
        super().__init__(source_url, source_type)

    def check(self):
        soup = self.get_soup()

        page_url = self.source_url[:self.source_url.rfind("/")]

        calendar = self.find_class(soup, "fullcalendar-content")
        if calendar is None:
            print(f"{calendar} is None")
            return
        titles = self.find_all(calendar, 'h3')
        dates = self.find_all(calendar, 'a')
        urls = [f"{page_url}{a_element.get('href')}" for a_element in self.find_all(calendar, "a") if a_element.get('href')]
        print(len(titles))

        for title, date, url in zip(titles, dates, urls):
            event = Event(self.source_url, self.source_type, title=title.get_text(strip=True), start=date.get_text(strip=True), url=url)
            self.events.append(event)
    
    def get_events(self):
        return self.events

class RSSChecker(Checker):
    def __init__(self, source_url, source_type):
        super().__init__(source_url, source_type)
    
    def check(self):
        soup = self.get_soup(features="xml")
        items = self.find_all(soup, 'item')
        for item in items:
            poster = self.find(item, "dc:creator").get_text(strip=True) if self.find(item, "dc:creator") is not None else ""
            title = self.find(item, "title").get_text() if self.find(item, "title") is not None else ""
            start = self.find(item, "pubDate").get_text() if self.find(item, "pubDate") is not None else ""
            end = self.find(item, "livewhale:ends").get_text() if self.find(item, "livewhale:ends") is not None else ""
            building = self.find(item, "georss:featurename").get_text(strip=True) if self.find(item, "georss:featurename") is not None else ""
            url = self.find(item, "link").get_text() if self.find(item, "link") is not None else ""
            
            self.events.append(Event(
                self.source_url, 
                self.source_type,
                poster=poster, 
                title=title, 
                start=start, 
                end=end,
                building=building,
                url=url
            ))

    def get_events(self):
        return self.events

# class ICSChecker(Checker):
#     def __init__(self, source_url, source_type):
#         super().__init__(source_url, source_type)

# def create_rss_events_list(items):
#     events = []
#     for item in items:
#         try:
#             title = item.title.text
#         except:
#             title = None

#         try:
#             date = item.pubDate.text
#         except:
#             date = None
        
#         try:
#             link = item.link.text
#         except:
#             link = None
#         events.append(database_format("",title,date,"","",link))
#     return events

rss = RSSChecker("https://financialaid.ucmerced.edu/rss.xml", "rss")
rss.check()
events = rss.get_events()
for event in events:
    print(f"{event.poster}, {event.title}, {event.start}, {event.end}, {event.building}, {event.url}")

# calendar = CalendarChecker("https://spanish.ucmerced.edu/events", "calendar")
# calendar.check()
# events = calendar.get_events()
# print(len(events))
# for event in events:
#     print(f"{event.title}, {event.start}, {event.url}")