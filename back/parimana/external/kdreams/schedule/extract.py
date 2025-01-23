from dataclasses import dataclass
import datetime
from typing import Sequence

from bs4 import BeautifulSoup, Tag


def extract_meeting_day_link(day_page_html: str) -> Sequence[str]:
    soup = BeautifulSoup(
        day_page_html.encode("utf-8"), "html.parser", from_encoding="utf-8"
    )
    anchors = soup.select("li.active ul.kaisai-list_sub-nav-list > li:nth-child(1) > a")
    return [a_tag.get("href") for a_tag in anchors]


@dataclass
class ExtractedRaceInfo:
    link: str
    poll_closing_time: datetime.time


def extract_races(meeting_day_page_html: str) -> Sequence[ExtractedRaceInfo]:
    soup = BeautifulSoup(
        meeting_day_page_html.encode("utf-8"), "html.parser", from_encoding="utf-8"
    )
    cards = soup.select("ul.racecard_list > li:not(.page-break)")
    return [extract_race_info(card) for card in cards]


def extract_race_info(race_card: Tag) -> ExtractedRaceInfo:
    race_link = race_card.select_one("p a").get("href")
    closing_time_text = race_card.select_one(
        "div.header > div.status.cf > dl > dd:nth-child(4)"
    ).get_text()
    closing_time = datetime.datetime.strptime(closing_time_text, "%H:%M").time()
    return ExtractedRaceInfo(race_link, closing_time)


def extract_closing_time(race_page_html: str) -> datetime.time:
    soup = BeautifulSoup(
        race_page_html.encode("utf-8"), "html.parser", from_encoding="utf-8"
    )
    closing_time_text = soup.select_one(
        "div.racecard_header > div > dl > dd:nth-child(4)"
    ).get_text()
    return datetime.datetime.strptime(closing_time_text, "%H:%M").time()
