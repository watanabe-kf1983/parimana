from typing import Collection, Iterator, Mapping, Tuple
import functools
from datetime import timedelta, datetime

import requests

from parimana.base import BettingType
from parimana.message import mprint
from parimana.race.boatrace.race import BoatRace
from parimana.driver.modest import ModestFunction


modestly = ModestFunction(interval=timedelta(seconds=1.5))


def get_source_uri(race: BoatRace) -> str:
    return _odds_page_uri(race, BettingType.TRIFECTA)


def browse_for_odds_timestamp(race: BoatRace) -> str:
    return browse_odds_page(race, BettingType.WIN)


def browse_odds_pages(
    race: BoatRace, attempt: str
) -> Iterator[Tuple[str, BettingType]]:
    for btype in supported_types:
        page_content = browse_odds_page(race, btype, attempt)
        yield (page_content, btype)


def browse_odds_page(race: BoatRace, btype: BettingType, attempt: str = "1st") -> str:
    uri = _odds_page_uri(race, btype)
    return _get(uri, f"{datetime.now():%Y%m%d%H%M}-{attempt}")


def browse_day_index(date: datetime.date) -> str:
    return _get(_day_index_page_uri(date), f"{datetime.now():%Y%m%d%H%M}")


def browse_schedule(date: datetime.date, jo_code: str) -> str:
    return _get(_race_schedule_page_uri(date, jo_code), f"{datetime.now():%Y%m%d%H%M}")


@functools.cache
@modestly
def _get(uri: str, attempt: str):
    mprint(f"opening {uri} ...")
    res = requests.get(uri)
    res.raise_for_status()
    text = res.text
    return text


def _odds_page_uri(race: BoatRace, btype: BettingType) -> str:
    return (
        f"https://www.boatrace.jp/owpc/pc/race/odds{btype_to_code(btype)}?"
        f"rno={race.race_no}&jcd={race.jo_code}&hd={race.date:%Y%m%d}"
    )


def _day_index_page_uri(date: datetime.date) -> str:
    return f"https://www.boatrace.jp/owpc/pc/race/index?hd={date:%Y%m%d}"


def _race_schedule_page_uri(date: datetime.date, jo_code: str) -> str:
    return (
        "https://www.boatrace.jp/owpc/pc/race/raceindex?"
        f"jcd={jo_code}&hd={date:%Y%m%d}"
    )


def btype_to_code(btype: BettingType) -> str:
    return _type_dict[btype]


_type_dict: Mapping[BettingType, str] = {
    BettingType.WIN: "tf",
    BettingType.PLACE: "tf",
    BettingType.EXACTA: "2tf",
    BettingType.QUINELLA: "2tf",
    BettingType.WIDE: "k",
    BettingType.TRIO: "3f",
    BettingType.TRIFECTA: "3t",
}

supported_types: Collection[BettingType] = _type_dict.keys()
