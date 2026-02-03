from checker import Checker, Event

class ListservChecker(Checker):
    def __init__(self, source_url):
        super().__init__(source_url, "listserv")
    
    def check(self):
        soup = self.get_soup()
        email_url = self.get_email_url(soup, self.source_url)
        if email_url is None:
            return None
        soup = self.get_soup(url=email_url)

        page_url = email_url[:email_url.rfind("/")+1]
        emails = soup.find_all("ul")[1]
        items = emails.find_all("li", recursive=False)
        authors = []
        subjects = []
        for item in items:
            authors.extend(item.find_all("i"))
            subjects.extend(item.find_all("a", href=True))
        for author, subject in zip(authors, subjects):
            poster = author.get_text(strip=True)
            title = subject.get_text(strip=True)
            html = subject.get('href')
            url = f"{page_url}{html}"
            self.events.append(Event(
                source_url=self.source_url,
                source_type=self.source_type,
                poster=poster,
                title=title,
                url=url
            ))

    def get_email_url(self, soup, url):
        table = soup.find('table')
        if (len(table.find_all('tr'))) <= 1:
            return None

        row = table.find_all('tr')[1]
        email_url = f"{url}{row.find('a').get('href')}"
        return email_url
    

# listserv = ListservChecker("https://lists.ucmerced.edu/pipermail/uctk/")
# listserv.check()
# events = listserv.get_events()
# for event in events[:10]:
#     output = ""
#     output += f"{event.poster}, " if event.poster is not None else ""
#     output += f"{event.title}, " if event.title is not None else ""
#     output += f"{event.start}, " if event.start is not None else ""
#     output += f"{event.end}, " if event.end is not None else ""
#     output += f"{event.building}, " if event.building is not None else ""
#     output += f"{event.url} " if event.url is not None else ""
#     print(output)