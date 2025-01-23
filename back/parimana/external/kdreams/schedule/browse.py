from datetime import datetime

from parimana.external.kdreams import browser
from parimana.external.kdreams.base import KeirinRace


def browse_day_index(date: datetime.date) -> str:
    return browser.get(_day_index_page_uri(date), f"{datetime.now():%Y%m%d%H%M}")


def browse_link(link: str) -> str:
    return browser.get(link, f"{datetime.now():%Y%m%d%H%M}")


def browse_race(race: KeirinRace) -> str:
    return browser.get(_race_detail_page_uri(race), f"{datetime.now():%Y%m%d%H%M}")


def _day_index_page_uri(date: datetime.date) -> str:
    return f"https://keirin.kdreams.jp/kaisai/{date:%Y/%m/%d}/"


def _race_detail_page_uri(race: KeirinRace) -> str:
    return (
        f"https://keirin.kdreams.jp/{race.meeting_day.meeting.studium.name_en}/"
        f"racedetail/{race.code}/"
    )
