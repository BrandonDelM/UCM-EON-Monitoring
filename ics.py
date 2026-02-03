from checker import Checker, Event
from icalendar import Calendar

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