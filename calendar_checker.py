from checker import Checker, Event
import requests
from bs4 import BeautifulSoup

class CalendarChecker(Checker):
    def __init__(self, source_url):
        super().__init__(source_url, "calendar")

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
            event = Event(self.source_url, self.source_type, title=title.get_text(strip=True), start=date.get_text(strip=True), url=url)
            self.events.append(event)