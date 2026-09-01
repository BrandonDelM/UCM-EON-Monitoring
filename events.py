from checker import Checker, Event
import json
import requests

class EventChecker(Checker):
    def __init__(self, source_url):
        super().__init__(source_url, "events")

    async def check(self):
        r = await self.get_request(self.source_url)
        print(type(r.text))
        events = json.loads(r.text)
        for event in events:
            url = f'https://ucmerced.presence.io/event/'
            title = event['eventName']
            poster = event['organizationName']
            building = event['location']
            start = event['startDateTimeUtc']
            end = event['endDateTimeUtc']
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

# checker = EventChecker('https://api.presence.io/ucmerced/v1/events')
# import asyncio
# asyncio.run(checker.check())
# from database import is_row_in_table
# for event in checker.events:
#     print(is_row_in_table(event))