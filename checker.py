import requests
from bs4 import BeautifulSoup
# from ics import Calendar
from icalendar import Calendar

class Event():
    def __init__(self, source_url, source_type, poster=None, title=None, start=None, end=None, building=None, url=None):
        self.source_url: str = source_url
        self.source_type: str = source_type
        self.poster = poster
        self.title = title
        self.start = start
        self.end = end
        self.building = building
        self.url = url

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
        r = self.get_request()
        soup = BeautifulSoup(r.text, features=features)
        return soup

    def get_request(self):
        return requests.get(self.source_url)
    
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

    def find_all_class(self, soup, check):
        if soup.find_all(class_=check):
            return soup.find_all(class_=check)
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
            poster = self.find(item, "dc:creator").get_text(strip=True) if self.find(item, "dc:creator") is not None else None
            title = self.find(item, "title").get_text() if self.find(item, "title") is not None else None
            start = self.find(item, "pubDate").get_text() if self.find(item, "pubDate") is not None else None
            end = self.find(item, "livewhale:ends").get_text() if self.find(item, "livewhale:ends") is not None else None
            building = self.find(item, "georss:featurename").get_text(strip=True) if self.find(item, "georss:featurename") is not None else None
            url = self.find(item, "link").get_text() if self.find(item, "link") is not None else None
            
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

class ICSChecker(Checker):
    def __init__(self, source_url, source_type):
        super().__init__(source_url, source_type)
    
    def check(self):
        r = self.get_request()
        cal = Calendar.from_ical(r.text)
        with open("test3.txt", "wb") as f:
            f.write(cal.to_ical())
        for event in cal.walk("VEVENT"):
            poster = event.get("ORGANIZER")

            poster = str(poster).strip() if poster is not None else None

            title = event.get("SUMMARY")
            title = str(title).strip() if title is not None else None

            start = event.get("DTSTART")
            start = start.dt.isoformat() if start else None

            end = event.get("DTEND")
            end = end.dt.isoformat() if end else None

            building = event.get("LOCATION")
            building = str(building).strip() if building is not None else None

            url = event.get("URL")
            url = str(url).strip() if url is not None else None

            self.events.append(Event(
                source_url=self.source_url,
                source_type=self.source_type,
                poster=poster,
                title=title,
                start=start,
                end=end,
                building=building,
                url=url
            ))

    def get_events(self):
        return self.events

class NewsChecker(Checker):
    def __init__(self, source_url, source_type):
        super().__init__(source_url, source_type)
    
    def check(self):
        soup = self.get_soup("html.parser")
        page_url = self.source_url[:self.source_url.rfind("/")]
        contents = self.find_class(soup, "view-content")
        events = self.find_all_class(contents, "views-row")
        for event in events[:1]:
            title = self.find(event, "a").get_text(strip=True) if self.find(event, "a") is not None else None
            start = self.find_class(event, "date-display-single").get("content") if self.find_class(event, "date-display-single") is not None else None
            url = self.find(event, "a").get("href") if self.find(event, "a") is not None else None
            url = f"{page_url}{url}" if url is not None else None
            self.events.append(Event(
                source_url=self.source_url,
                source_type=self.source_type,
                title=title,
                start=start,
                url=url
            ))
        
        
    def get_events(self):
        return self.events

class YouTubeChecker(Checker):
    def __init__(self, source_url, source_type):
        super().__init__(source_url, source_type)
    
    def check(self):
        soup = self.get_soup("xml")
        entries = self.find_all(soup, "entry")
        for entry in entries:
            
            author = self.find(entry, "author") if self.find(entry, "author") is not None else None
            poster = self.find(author, "name").get_text(strip=True) if self.find(author, "name") is not None else None

            title = self.find(entry, "title").get_text(strip=True) if self.find(entry, "title") is not None else None
            start = self.find(entry, "published").get_text() if self.find(entry, "published") is not None else None

            youtube_id = self.find(entry, "yt:videoId") if self.find(entry, "yt:videoId") is not None else None
            url = f"http://youtu.be/{youtube_id.get_text()}" if youtube_id is not None else None
            
            self.events.append(Event(
                source_url=self.source_url,
                source_type=self.source_type,
                poster=poster,
                title=title,
                start=start,
                url=url
            ))
        return

    def get_events(self):
        return self.events

youtube = YouTubeChecker("https://www.youtube.com/feeds/videos.xml?channel_id=UCijMqBPttHFTv7O_mhhsjjg", "youtube")
youtube.check()
events = youtube.get_events()
for event in events[:10]:
    output = ""
    output += f"{event.poster}, " if event.poster is not None else ""
    output += f"{event.title}, " if event.title is not None else ""
    output += f"{event.start}, " if event.start is not None else ""
    output += f"{event.end}, " if event.end is not None else ""
    output += f"{event.building}, " if event.building is not None else ""
    output += f"{event.url} " if event.url is not None else ""
    print(output)