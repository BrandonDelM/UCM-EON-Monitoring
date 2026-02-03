from checker import Checker, Event

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