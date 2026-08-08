from checker import Checker, Event
import requests
from bs4 import BeautifulSoup

class NewsChecker(Checker):
    def __init__(self, source_url):
        super().__init__(source_url, "news")
    
    async def check(self):
        # soup = await self.get_soup(url=self.source_url, features="html.parser")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
            "Accept-Language": "en-US,en;q=0.9",
        }
        request = requests.get(self.source_url, headers=headers)
        soup = BeautifulSoup(request.text,"html.parser")
        
        page_url = self.source_url[:self.source_url.rfind("/")]

        contents = soup.find(class_="view-content")
        if contents is None:
            print(f"{self.source_url} returns a None")
            return
        events = contents.find_all(class_="views-row")

        for event in events:
            title = event.find("a").get_text(strip=True) if event.find("a") is not None else None
            start = event.find(class_="date-display-single").get("content") if event.find(class_="date-display-single") is not None else None

            url = event.find("a").get("href") if event.find("a") is not None else None
            url = f"{page_url}{url}" if url is not None else None

            self.events.append(Event(
                source_url=self.source_url,
                source_type=self.source_type,
                title=title,
                start=start,
                url=url
            ))