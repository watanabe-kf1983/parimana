from dataclasses import dataclass
from typing import Optional, Sequence
import datetime
import re

from bs4 import BeautifulSoup, Tag

from parimana.external.boatrace.schedule.base import BoatRaceJo

IMG_JO_CODE_PATTERN: re.Pattern = re.compile(r"text_place1_(?P<jo_code>[0-9]{2})\.png")
RACE_NO_PATTERN: re.Pattern = re.compile(r"rno=(?P<race_no>[0-9]{1,2})")


@dataclass
class SimpleRaceInfo:
    race_no: int
    name: str
    poll_closing_time: datetime.time


def extract_joes(day_page_html: str) -> Sequence[BoatRaceJo]:
    soup = BeautifulSoup(
        day_page_html.encode("utf-8"), "html.parser", from_encoding="utf-8"
    )
    table = soup.select_one("div.contentsFrame1_inner > div.table1 > table")
    imgs = table.select(
        "tbody > tr:nth-child(1) > td.is-arrow1.is-fBold.is-fs15 > a > img"
    )
    return list(filter(bool, (_extract_jo_from_imgtag(i) for i in imgs)))


def _extract_jo_from_imgtag(img: Tag) -> Optional[BoatRaceJo]:
    name = img.get("alt")
    code_match = re.search(IMG_JO_CODE_PATTERN, img.get("src"))
    if name and code_match:
        jo_code = code_match.group("jo_code")
        return BoatRaceJo(jo_code, name)


def extract_races(schedule_page_html: str) -> Sequence[SimpleRaceInfo]:
    soup = BeautifulSoup(
        schedule_page_html.encode("utf-8"), "html.parser", from_encoding="utf-8"
    )
    table = soup.select_one("div.contentsFrame1_inner > div.table1 > table")
    rows = table.select("tbody > tr")
    return list(filter(bool, (_extract_race_from_tr(tr) for tr in rows)))


def _extract_race_from_tr(tr: Tag) -> Optional[SimpleRaceInfo]:
    race_anchor = tr.select_one("td:nth-child(1) > a")
    race_name = race_anchor.get_text(strip=True)
    race_no = int(re.search(RACE_NO_PATTERN, race_anchor.get("href")).group("race_no"))
    closing_time_text = tr.select_one("td:nth-child(2)").get_text(strip=True)
    closing_time = datetime.datetime.strptime(closing_time_text, "%H:%M").time()
    return SimpleRaceInfo(race_no, race_name, closing_time)
