from checker import Checker, Event
from dateutil import parser

class YouTubeChecker(Checker):
    def __init__(self, source_url):
        super().__init__(source_url, "youtube")
    
    async def check(self):
        soup = await self.get_soup(self.source_url, "xml")
        if soup is None:
            print(f"{self.source_url} return with {soup}")
            return None
        entries = soup.find_all("entry")
        for entry in entries:
            
            author = entry.find("author") if entry.find("author") is not None else None
            poster = author.find("name").get_text(strip=True) if author.find("name") is not None else None

            title = entry.find("title").get_text(strip=True) if entry.find("title") is not None else None
            start = entry.find("published").get_text() if entry.find("published") is not None else None
            dt = parser.parse(start)
            start = dt.isoformat()

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