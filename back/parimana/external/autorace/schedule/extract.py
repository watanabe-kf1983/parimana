import datetime
import re

from bs4 import BeautifulSoup


def has_contents(page_html: str) -> bool:
    try:
        extract_closing_time(page_html)
        return True
    except ValueError:
        return False


def extract_closing_time(page_html: str) -> datetime.timedelta:
    soup = parse(page_html)
    race_text = soup.select_one("#race-result-current-race-telvote").get_text()
    if m := re.search(CLOSING_TIME_PATTERN, race_text):
        # hour may be 24 or 25 at midnight
        return datetime.timedelta(
            hours=int(m.group("hour")), minutes=int(m.group("minute"))
        )
    else:
        raise ValueError("Failed parse closing time string: " + race_text)


def parse(html: str) -> BeautifulSoup:
    return BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")


CLOSING_TIME_PATTERN: re.Pattern = re.compile(
    r"投票締切\s*(?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{2})"
)
