from checker import Checker, Event

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