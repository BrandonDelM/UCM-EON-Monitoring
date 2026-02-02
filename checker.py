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

class CalendarChecker(Checker):
    def __init__(self, source_url):
        super().__init__(source_url, "calendar")

    def check(self):
        soup = self.get_soup()

        page_url = self.source_url[:self.source_url.rfind("/")]

        calendar = soup.find(class_="fullcalendar-content")
        if calendar is None:
            print(f"{calendar} is None")
            return
        titles = calendar.find_all('h3')
        dates = calendar.find_all('a')
        urls = [f"{page_url}{a_element.get('href')}" for a_element in calendar.find_all("a") if a_element.get('href')]
        print(len(titles))

        for title, date, url in zip(titles, dates, urls):
            event = Event(self.source_url, self.source_type, title=title.get_text(strip=True), start=date.get_text(strip=True), url=url)
            self.events.append(event)
    
    def get_events(self):
        return self.events

class RSSChecker(Checker):
    def __init__(self, source_url):
        super().__init__(source_url, "rss")
    
    def check(self):
        soup = self.get_soup(features="xml")
        items = soup.find_all('item')
        for item in items:
            poster = item.find("dc:creator").get_text(strip=True) if item.find("dc:creator") is not None else None
            title = item.find("title").get_text() if item.find("title") is not None else None
            start = item.find("pubDate").get_text() if item.find("pubDate") is not None else None
            end = item.find("livewhale:ends").get_text() if item.find("livewhale:ends") is not None else None
            building = item.find("georss:featurename").get_text(strip=True) if item.find("georss:featurename") is not None else None
            url = item.find("link").get_text() if item.find("link") is not None else None
            
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
    def __init__(self, source_url):
        super().__init__(source_url, "ics")
    
    def check(self):
        r = self.get_request()
        cal = Calendar.from_ical(r.text)
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
    def __init__(self, source_url):
        super().__init__(source_url, "news")
    
    def check(self):
        soup = self.get_soup("html.parser")
        page_url = self.source_url[:self.source_url.rfind("/")]
        contents = soup.find(class_="view-content")
        events = contents.find_all(class_="views-row")
        for event in events[:1]:
            title = event.find("a").get_text(strip=True) if event.find("a") is not None else None
            start = event.find_class("date-display-single").get("content") if event.find_class("date-display-single") is not None else None
            url = event.find("a").get("href") if event.find("a") is not None else None
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
    def __init__(self, source_url):
        super().__init__(source_url, "youtube")
    
    def check(self):
        soup = self.get_soup("xml")
        entries = soup.find_all("entry")
        for entry in entries:
            
            author = entry.find("author") if entry.find("author") is not None else None
            poster = entry.find(author, "name").get_text(strip=True) if entry.find(author, "name") is not None else None

            title = entry.find("title").get_text(strip=True) if entry.find("title") is not None else None
            start = entry.find("published").get_text() if entry.find("published") is not None else None

            youtube_id = entry.find("yt:videoId") if entry.find("yt:videoId") is not None else None
            url = f"http://youtu.be/{youtube_id.get_text()}" if youtube_id is not None else None
            
            self.events.append(Event(
                source_url=self.source_url,
                source_type=self.source_type,
                poster=poster,
                title=title,
                start=start,
                url=url
            ))

    def get_events(self):
        return self.events

class ListservChecker(Checker):
    def __init__(self, source_url):
        super().__init__(source_url, "listserv")
    
    def check(self):
        soup = self.get_soup()
        email_url = self.get_email_url(soup, self.source_url)
        if email_url is None:
            return None
        soup = self.get_soup(url=email_url)

        page_url = email_url[:email_url.rfind("/")+1]
        emails = soup.find_all("ul")[1]
        items = emails.find_all("li", recursive=False)
        authors = []
        subjects = []
        for item in items:
            authors.extend(item.find_all("i"))
            subjects.extend(item.find_all("a", href=True))
        for author, subject in zip(authors, subjects):
            poster = author.get_text(strip=True)
            title = subject.get_text(strip=True)
            html = subject.get('href')
            url = f"{page_url}{html}"
            self.events.append(Event(
                source_url=self.source_url,
                source_type=self.source_type,
                poster=poster,
                title=title,
                url=url
            ))

    def get_email_url(self, soup, url):
        table = soup.find('table')
        if (len(table.find_all('tr'))) <= 1:
            return None

        row = table.find_all('tr')[1]
        email_url = f"{url}{row.find('a').get('href')}"
        return email_url
    
    def get_events(self):
        return self.events

listserv = ListservChecker("https://lists.ucmerced.edu/pipermail/uctk/")
listserv.check()
events = listserv.get_events()
for event in events[:10]:
    output = ""
    output += f"{event.poster}, " if event.poster is not None else ""
    output += f"{event.title}, " if event.title is not None else ""
    output += f"{event.start}, " if event.start is not None else ""
    output += f"{event.end}, " if event.end is not None else ""
    output += f"{event.building}, " if event.building is not None else ""
    output += f"{event.url} " if event.url is not None else ""
    print(output)