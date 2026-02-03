from checker import Checker, Event

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