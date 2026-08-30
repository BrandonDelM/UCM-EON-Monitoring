from checker import Checker, Event
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

class CepChecker(Checker):
    def __int__(self, source_url):
        super().__init__(source_url, "cep")

    def put_time_format(self, time):
        formats = ["%I:%M%p","%I:%M"]
        for format in formats:
            try:
                return datetime.strptime(time, format).time()
            except Exception as e:
                continue

    async def check(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
            "Accept-Language": "en-US,en;q=0.9",
        }
        r = await self.get_request(self.source_url, headers=headers)
        if r is None:
            print(f"{self.source_url} return with {r}")
            return None
        if r.status_code == 200:
            events = r.json()
        else:
            return "Couldn't retrieve data for cep", 400
        
        unique_events = list({event['idActivity']: event for event in events}.values())

        for event in unique_events:
            title: str = event['name']
            building: str = event['location']
            start = event['dateExpected']
            end = None

            if event['timeFrom'] and event['timeTo'] is not None:
                event_from: str = event['timeFrom'].replace(" ", "")
                event_to: str = event['timeTo'].replace(" ", "")
                date = datetime.fromisoformat(event['dateExpected'].replace("Z", "+00:00")).date()

                start_from = self.put_time_format(event_from)
                end_to = self.put_time_format(event_to)

                zone = ZoneInfo("America/Los_Angeles")
                start = datetime.combine(date, start_from, zone).isoformat()
                end = datetime.combine(date, end_to, zone).isoformat()
            
            id = event['idActivity']
            url = f"https://ucmcep.org/events/{id}"
            event = Event(
                self.source_url,
                self.source_type,
                title=title,
                start=start,
                end=end,
                building=building,
                url=url
            )
            self.events.append(event)

# checker = CepChecker("https://ucmcep.org/api/cep/calendar?dateFrom=1%2F1%2F2026", "cep")
# import asyncio
# asyncio.run(checker.check())
# for event in checker.events:
#     print(event.title, event.start, event.end, event.building, event.url)