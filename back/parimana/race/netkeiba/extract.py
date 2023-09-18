from typing import Mapping
from datetime import datetime
from zoneinfo import ZoneInfo
import re

from bs4 import BeautifulSoup

from parimana.base import BettingType, Eye, Odds, PlaceOdds, OddsTimeStamp
from parimana.race.netkeiba.btype import code_to_btype, btype_to_code


# <span id="official_time">13:33(142分前)</span>
UPDATE_PATTERN: re.Pattern = re.compile(r"(?P<time>[0-9]{1,2}:[0-9]{2})\([0-9]+分前\)")

jst = ZoneInfo("Asia/Tokyo")


def extract_timestamp(html: str) -> OddsTimeStamp:
    soup = BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")
    upd_btn = soup.select_one("#act-manual_update")
    text = soup.select_one("#official_time").get_text()

    if upd_btn.has_attr("style") and "display:none" in upd_btn["style"]:
        return OddsTimeStamp.confirmed

    elif m := re.fullmatch(UPDATE_PATTERN, text):
        today = datetime.now(jst).date()
        time = datetime.strptime(m.group("time"), "%H:%M")
        dt = datetime.combine(today, time.time(), jst)
        return OddsTimeStamp(dt)

    else:
        raise ValueError("Failed parse update time string: " + text)


def extract_odds(html: str, btype: BettingType) -> Mapping[Eye, float]:
    soup = BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")
    elements = soup.select(f"table td.Odds span[id^='odds-{btype_to_code(btype)}']")
    odds = _elements_to_odds(elements)

    if btype == BettingType.WIDE:
        elementsmax = soup.select(
            f"table td.Odds span[id^='oddsmin-{btype_to_code(btype)}']"
        )
        oddsmax = _elements_to_odds(elementsmax)
        odds = {e: PlaceOdds(odds[e].odds_, oddsmax[e].odds_) for e in odds.keys()}

    return odds


def _elements_to_odds(elements):
    return {_elem_id_to_eye(e["id"]): Odds.from_text(e.get_text()) for e in elements}


def _elem_id_to_eye(id: str):
    _, btype_code, number = id.replace("_", "-").split("-")
    betting_type = code_to_btype(btype_code)
    names = [number[i : i + 2] for i in range(0, len(number), 2)]
    return Eye.from_names(names, betting_type)
