from checker import Checker, Event
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

class CalendarChecker(Checker):
    def __init__(self, source_url):
        super().__init__(source_url, "calendar")

    def put_iso_to_utc(self, time):
        if time is None:
            return None
        try:
            return datetime.fromisoformat(time).astimezone(timezone.utc).isoformat()
        except Exception:
            return time

    async def check(self):
        # soup = await self.get_soup(self.source_url)
        # print(soup)

        #Temporary solution as original solution got blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
            "Accept-Language": "en-US,en;q=0.9",
        }
        request = requests.get(self.source_url, headers=headers)
        soup = BeautifulSoup(request.text,"html.parser")

        page_url = self.source_url[:self.source_url.rfind("/")]

        calendar = soup.find(class_="fullcalendar-content")
        if calendar is None:
            print(f"{self.source_url} returns a None")
            return
        titles = calendar.find_all('h3')
        dates = calendar.find_all('a')
        urls = [f"{page_url}{a_element.get('href')}" for a_element in calendar.find_all("a") if a_element.get('href')]

        for title, date, url in zip(titles, dates, urls):
            start = date.find(class_='date-display-start').get('content') if date.find(class_='date-display-start') else None
            start = self.put_iso_to_utc(start)

            end = date.find(class_='date-display-end').get('content') if date.find(class_='date-display-end') else None
            end = self.put_iso_to_utc(end)

            if start is None:
                start = date.find(class_='date-display-single').get('content') if date.find(class_='date-display-single') else None
                start = self.put_iso_to_utc(start)

            event = Event(self.source_url, self.source_type, title=title.get_text(strip=True), start=start, end=end, url=url)
            self.events.append(event)