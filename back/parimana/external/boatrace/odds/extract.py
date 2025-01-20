from typing import Mapping, Optional, Sequence
from datetime import datetime
import re

from bs4 import BeautifulSoup, Tag
import numpy as np

from parimana.domain.base import BettingType, Eye, Odds
from parimana.domain.race import OddsTimeStamp
from parimana.external.boatrace.base import category_boat

UPDATE_PATTERN: re.Pattern = re.compile(
    r"\s*オッズ更新時間\s*(?P<time>[0-9]{1,2}:[0-9]{2})\s*"
)


def extract_timestamp(html: str) -> OddsTimeStamp:
    text = update_time_text(html)
    if text == "締切時オッズ":
        return OddsTimeStamp.confirmed()

    elif m := re.fullmatch(UPDATE_PATTERN, text):
        tz = category_boat.timezone
        today = datetime.now(tz).date()
        time = datetime.strptime(m.group("time"), "%H:%M")
        dt = datetime.combine(today, time.time(), tz)
        return OddsTimeStamp(dt)

    else:
        raise ValueError("Failed parse update time string: " + text)


def update_time_text(html: str) -> str:
    soup = BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")
    return soup.select_one("p.tab4_refreshText, p.tab4_time").get_text(strip=True)


def extract_odds(html: str, btype: BettingType) -> Mapping[Eye, Odds]:
    soup = BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")
    table = select_table(btype, soup)
    extracted = extract_odds_from_table(table)
    eyes = eyes_table_order(btype)
    return {eye: odds for eye, odds in zip(eyes, extracted) if odds}


def select_table(btype: BettingType, soup: BeautifulSoup) -> Tag:
    if btype == BettingType.WIN:
        return soup.select_one(
            "div.contentsFrame1_inner > "
            "div.grid.is-type2.h-clear > div:nth-child(1) table"
        )
    elif btype == BettingType.PLACE:
        return soup.select_one(
            "div.contentsFrame1_inner > "
            "div.grid.is-type2.h-clear > div:nth-child(2) table"
        )
    elif btype == BettingType.QUINELLA:
        return soup.select_one(
            "div.contentsFrame1_inner > div:nth-child(n+9):nth-child(-n+10) table"
        )
    else:
        return soup.select_one(
            "div.contentsFrame1_inner > div:nth-child(n+7):nth-child(-n+8) table"
        )


def extract_odds_from_table(table: Tag) -> Sequence[Optional[Odds]]:
    return [_try_parse_odds(e.get_text()) for e in table.select("td.oddsPoint")]


def _try_parse_odds(odds_text: str) -> Optional[Odds]:
    try:
        return Odds.from_text(odds_text())
    except Exception:  # "欠場"
        return None


def eyes_table_order(btype: BettingType) -> Sequence[Eye]:
    names = [str(n) for n in range(1, 7)]
    all_eyes = Eye.all_eyes(names, btype)
    if btype.size == 1:  # win, place, show
        return all_eyes
    elif btype.sequencial:  # exacta, trifecta
        return np.array(all_eyes).reshape(6, -1).T.reshape(-1).tolist()
    else:
        if btype.size == 2:  # wide, quinella
            return sorted(
                all_eyes, key=lambda e: sorted(e.names)[1] + sorted(e.names)[0]
            )
        else:  # trio
            return sorted(
                all_eyes,
                key=lambda e: sorted(e.names)[1]
                + sorted(e.names)[2]
                + sorted(e.names)[0],
            )
