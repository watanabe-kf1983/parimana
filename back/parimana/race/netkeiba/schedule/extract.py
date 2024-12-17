from dataclasses import dataclass
import re
from typing import Sequence

from bs4 import BeautifulSoup, Tag


@dataclass
class RaceListItem:
    keibajo_code: str
    race_num_text: str
    title: str
    start_time_text: str
    netkeiba_race_id: str


def extract_open_days(calendar_page_html: str) -> Sequence[int]:
    soup = BeautifulSoup(
        calendar_page_html.encode("utf-8"), "html.parser", from_encoding="utf-8"
    )
    elements = soup.select("div.Race_Calendar_Main div.RaceKaisaiBox.HaveData span.Day")
    return [int(e.get_text(strip=True)) for e in elements]


def extract_schedule(schedule_page_html: str) -> Sequence[RaceListItem]:
    soup = BeautifulSoup(
        schedule_page_html.encode("utf-8"), "html.parser", from_encoding="utf-8"
    )
    anchors = soup.select("#RaceTopRace li.RaceList_DataItem > a:nth-child(1)")
    return [extract_race_info(a_tag) for a_tag in anchors]


def extract_race_info(a_tag: Tag) -> RaceListItem:
    href = a_tag.get("href")
    if m := re.search(_NETKEIBA_RACE_ID_LINK, href):
        netkeiba_race_id = m.group("netkeiba_race_id")
    else:
        raise ValueError("Failed parse link: " + href)

    m2 = re.fullmatch(_NETKEIBA_RACE_ID_PATTERN, netkeiba_race_id)
    keibajo_code = m2.group("keibajo_code")
    race_num_text = a_tag.select_one("div.Race_Num > span").get_text(strip=True)
    title = a_tag.select_one("div.RaceList_ItemTitle > span.ItemTitle").get_text()
    start_time_text = a_tag.select_one("span.RaceList_Itemtime").get_text(strip=True)

    return RaceListItem(
        keibajo_code=keibajo_code,
        race_num_text=race_num_text,
        title=title,
        start_time_text=start_time_text,
        netkeiba_race_id=netkeiba_race_id,
    )


_NETKEIBA_RACE_ID_LINK: re.Pattern = re.compile(
    r"race_id=(?P<netkeiba_race_id>[0-9]{12})"
)


_NETKEIBA_RACE_ID_PATTERN: re.Pattern = re.compile(
    r"(?P<year>[0-9]{4})"
    r"(?P<keibajo_code>[0-9]{2})"
    r"(?P<kaisai_no>[0-9]{2})"
    r"(?P<day_no>[0-9]{2})"
    r"(?P<race_no>[0-9]{2})"
)
