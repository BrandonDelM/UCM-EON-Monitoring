## Monitoring for the UCM Events, Opportunities, and News RESTful API.
* Uses Supabase as the database for the API
* Similar monitoring as found in the Discord bot
* Will be used for the API, which will be used on other UC Merced projects and the Discord bot.

## File documentation:
### aaiscloud.py
Polls the following data using the api:
* EventMeetingByActivityId.Event.Customer.Name - poster
* ActivityName - title
* StartDateTime - start
* EndDateTime - end
* LocationName - building
* ActivityId - url

Currently limits query to just one day, but has been tested to grab events a month from the current day of monitoring.

**build_aaiscloud_calendar_url** returns the constructed url and **get_aaiscloud_headers** returns the necesssary headers for the request. The request returns a json which is used to retrieve event data.

## Todos:
- News should check in certain circumstances for information inside of a link for date ✅
- Listserv should check for the isoformat date ✅
- Calendar should check for location information with event link
- Add a more advance query which checks if the database already contains an event.
- Implementation of Eventbrite into the monitoring system
- Implementation of Selenium into more complex monitoring (Infoready, etc.)