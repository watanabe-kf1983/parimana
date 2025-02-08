from dataclasses import dataclass
import datetime
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


class JraScheduleExtractor:

    def extract_open_days(self, calendar_page_html: str) -> Sequence[int]:
        soup = parse(calendar_page_html)
        kaisai_boxes = soup.select("div.Race_Calendar_Main div.RaceKaisaiBox")
        calendar = []
        for kaisai_box in kaisai_boxes:
            joes = kaisai_box.select("span.JyoName")
            if len(joes):
                span_day = kaisai_box.select_one("span.Day")
                calendar.append(int(span_day.get_text(strip=True)))

        return calendar

    def extract_schedule(self, schedule_page_html: str) -> Sequence[RaceListItem]:
        soup = parse(schedule_page_html)
        anchors = soup.select("#RaceTopRace li.RaceList_DataItem > a:nth-child(1)")
        return [self._extract_race_info(a_tag) for a_tag in anchors]

    def extract_race_date(self, race_page_html: str) -> datetime.date:
        soup = parse(race_page_html)
        schedule_link = soup.select_one("#RaceList_DateList > dd.Active > a").get(
            "href"
        )
        if m := re.search(_NETKEIBA_KAISAI_DATE_LINK, schedule_link):
            return datetime.datetime.strptime(m.group("kaisai_date"), "%Y%m%d").date()

        else:
            raise ValueError("Failed parse link: " + schedule_link)

    def _extract_race_info(self, a_tag: Tag) -> RaceListItem:
        href = a_tag.get("href")
        if m := re.search(_NETKEIBA_RACE_ID_LINK, href):
            netkeiba_race_id = m.group("netkeiba_race_id")
        else:
            raise ValueError("Failed parse link: " + href)

        keibajo_code = netkeiba_race_id[4:6]
        race_num_text = a_tag.select_one("div.Race_Num > span").get_text(strip=True)
        title = a_tag.select_one("div.RaceList_ItemTitle > span.ItemTitle").get_text()
        start_time_text = a_tag.select_one("span.RaceList_Itemtime").get_text(
            strip=True
        )

        return RaceListItem(
            keibajo_code=keibajo_code,
            race_num_text=race_num_text,
            title=title,
            start_time_text=start_time_text,
            netkeiba_race_id=netkeiba_race_id,
        )


class NarScheduleExtractor:

    def extract_schedule(self, schedule_page_html: str) -> Sequence[RaceListItem]:
        soup = parse(schedule_page_html)
        anchors = soup.select("#RaceTopRace li.RaceList_DataItem > a:nth-child(1)")
        return [self._extract_race_info(a_tag) for a_tag in anchors]

    def extract_schedule_kaisai_id(self, schedule_page_html: str) -> Sequence[str]:
        soup = parse(schedule_page_html)
        anchors = soup.select("#RaceTopRace ul.RaceList_ProvinceSelect a")
        return [self._extract_kaisai_id(a_tag) for a_tag in anchors]

    def _extract_race_info(self, a_tag: Tag) -> RaceListItem:
        href = a_tag.get("href")
        if m := re.search(_NETKEIBA_RACE_ID_LINK, href):
            netkeiba_race_id = m.group("netkeiba_race_id")
        else:
            raise ValueError("Failed parse link: " + href)

        keibajo_code = netkeiba_race_id[4:6]
        race_num_text = a_tag.select_one("div.Race_Num > span").get_text(strip=True)
        title = a_tag.select_one("div.RaceList_ItemTitle > span.ItemTitle").get_text()
        start_time_text = a_tag.select_one("div.RaceData > span:nth-child(1)").get_text(
            strip=True
        )

        return RaceListItem(
            keibajo_code=keibajo_code,
            race_num_text=race_num_text,
            title=title,
            start_time_text=start_time_text,
            netkeiba_race_id=netkeiba_race_id,
        )

    def _extract_kaisai_id(self, a_tag: Tag) -> str:
        href = a_tag.get("href")
        if m := re.search(_NETKEIBA_KAISAI_ID_LINK, href):
            return m.group("kaisai_id")
        else:
            raise ValueError("Failed parse link: " + href)


def parse(html: str) -> BeautifulSoup:
    return BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")


_NETKEIBA_KAISAI_DATE_LINK: re.Pattern = re.compile(
    r"kaisai_date=(?P<kaisai_date>[0-9]{8})"
)

_NETKEIBA_KAISAI_ID_LINK: re.Pattern = re.compile(r"kaisai_id=(?P<kaisai_id>[0-9]{10})")

_NETKEIBA_RACE_ID_LINK: re.Pattern = re.compile(
    r"race_id=(?P<netkeiba_race_id>[0-9]{12})"
)
