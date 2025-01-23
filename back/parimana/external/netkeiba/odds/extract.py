from abc import ABC, abstractmethod
from typing import Collection, Mapping, Optional
from datetime import datetime
from zoneinfo import ZoneInfo
import re

from bs4 import BeautifulSoup, Tag

from parimana.domain.base import BettingType, Eye, Odds, PlaceOdds
from parimana.domain.race import OddsTimeStamp
from parimana.external.netkeiba.odds.btype import code_to_btype, btype_to_code


# <span id="official_time">13:33(142分前)</span>
UPDATE_PATTERN: re.Pattern = re.compile(r"(?P<time>[0-9]{1,2}:[0-9]{2})\([0-9-]+分前\)")

# 13:33発走
START_TIME_PATTERN: re.Pattern = re.compile(r"(?P<time>[0-9]{1,2}:[0-9]{2})発走")

jst = ZoneInfo("Asia/Tokyo")


class NetKeibaOddsExtractor(ABC):
    @abstractmethod
    def extract_timestamp(self, html: str) -> OddsTimeStamp:
        pass

    @abstractmethod
    def extract_odds(self, html: str, btype: BettingType) -> Mapping[Eye, Odds]:
        pass


class JraOddsExtractor(NetKeibaOddsExtractor):
    def extract_timestamp(self, html: str) -> OddsTimeStamp:
        soup = BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")
        upd_btn = soup.select_one("#act-manual_update")
        text = soup.select_one("#official_time").get_text()

        if upd_btn.has_attr("style") and "display:none" in upd_btn["style"]:
            return OddsTimeStamp.confirmed()

        elif m := re.fullmatch(UPDATE_PATTERN, text):
            today = datetime.now(jst).date()
            time = datetime.strptime(m.group("time"), "%H:%M")
            dt = datetime.combine(today, time.time(), jst)
            return OddsTimeStamp(dt)

        else:
            raise ValueError("Failed parse update time string: " + text)

    def extract_odds(self, html: str, btype: BettingType) -> Mapping[Eye, Odds]:
        soup = BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")
        elements = soup.select(f"table td.Odds span[id^='odds-{btype_to_code(btype)}']")
        odds = _elements_to_odds(elements)

        if btype == BettingType.WIDE:
            elementsmax = soup.select(
                f"table td.Odds span[id^='oddsmin-{btype_to_code(btype)}']"
            )
            oddsmax = _elements_to_odds(elementsmax)
            odds = {e: PlaceOdds(odds[e].odds_, oddsmax[e].odds_) for e in odds.keys()}

        odds = _convert_show_to_place(odds)
        return odds


class NarOddsExtractor(NetKeibaOddsExtractor):
    def extract_start_datetime(self, html: str) -> datetime:
        soup = BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")
        date_link = soup.select_one("#RaceList_DateList > dd.Active > a").get("href")
        race_text = soup.select_one("div.RaceList_NameBox div.RaceData01").get_text()

        if m := re.search(_NETKEIBA_KAISAI_DATE_LINK, date_link):
            start_date = datetime.strptime(m.group("kaisai_date"), "%Y%m%d").date()
        else:
            raise ValueError("Failed parse link: " + date_link)

        if m := re.search(START_TIME_PATTERN, race_text):
            start_time = datetime.strptime(m.group("time"), "%H:%M").time()
        else:
            raise ValueError("Failed parse start time: " + race_text)

        return datetime.combine(start_date, start_time, jst)

    def extract_timestamp(self, html: str) -> Optional[OddsTimeStamp]:
        # nar.netkeiba.comは 更新時刻を表示しないので 発走時刻前なら現在時刻を返す
        start_dt = self.extract_start_datetime(html)
        now = datetime.now(jst).replace(second=0, microsecond=0)

        # 現在時刻を3分単位で切り捨て
        now_trunc = now.replace(
            minute=now.minute - (now.minute % 3), second=0, microsecond=0
        )

        if start_dt < now_trunc:
            return OddsTimeStamp.confirmed()
        else:
            return OddsTimeStamp(now_trunc)

    def extract_odds(self, html: str, btype: BettingType) -> Mapping[Eye, Odds]:
        soup = BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")
        div = _select_nar_odds_div(soup, btype)
        elements = div.select("table td.Odds")
        odds = _elements_to_odds_nar(elements, btype)

        odds = _convert_show_to_place(odds)
        return odds


_NETKEIBA_KAISAI_DATE_LINK: re.Pattern = re.compile(
    r"kaisai_date=(?P<kaisai_date>[0-9]{8})"
)


def _convert_show_to_place(odds: Mapping[Eye, Odds]) -> Mapping[Eye, Odds]:

    # 7頭立て以下の場合は複勝は2着まで
    # https://www.jra.go.jp/kouza/yougo/w432.html
    if (
        1 <= len(odds) <= 7
        and next(iter(odds.keys())).type == BettingType.SHOW
        and all(int(next(iter(eye.names))) <= 7 for eye in odds.keys())
        # 制限事項：8番以降が全部除外になって7頭になった場合も複勝は2着まで扱いになってしまう
        # 気になる場合は 頑張って何頭立てか調べるように直す
    ):
        return {
            Eye.from_names(list(e.names), BettingType.PLACE): o for e, o in odds.items()
        }
    else:
        return odds


def _select_nar_odds_div(soup: BeautifulSoup, btype: BettingType) -> Tag:
    if btype == BettingType.WIN:
        return soup.select_one("#odds_tan_block")
    elif btype == BettingType.SHOW:
        return soup.select_one("#odds_fuku_block")
    else:
        return soup.select_one("#odds_view_form div.GraphOdds")


def _elements_to_odds(elements):
    return {_elem_id_to_eye(e["id"]): Odds.from_text(e.get_text()) for e in elements}


def _elem_id_to_eye(id: str):
    _, btype_code, number = id.replace("_", "-").split("-")
    betting_type = code_to_btype(btype_code)
    names = [number[i : i + 2] for i in range(0, len(number), 2)]
    return Eye.from_names(names, betting_type)


def _elements_to_odds_nar(elements: Collection[Tag], btype: BettingType):
    def is_valid_odds(text: str):
        return bool(re.fullmatch(r"[\-\.0-9]+", text))

    if btype.size == 1:
        return {
            Eye.from_names([f"{int(i+1):02}"], btype): (
                Odds.from_text(e.get_text(strip=True))
            )
            for i, e in enumerate(elements)
            if is_valid_odds(e.get_text(strip=True))
        }
    else:
        return {
            _elem_id_to_eye_nar(e["id"], btype): (
                Odds.from_text(e.get_text(strip=True))
            )
            for e in elements
            if is_valid_odds(e.get_text(strip=True))
        }


def _elem_id_to_eye_nar(id: str, btype: BettingType):
    if btype.size > 1:
        num_texts = id.split("_")[-btype.size :]
        names = [f"{int(num_text):02}" for num_text in num_texts]
        return Eye.from_names(names, btype)
