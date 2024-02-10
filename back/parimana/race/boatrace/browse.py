from typing import Collection, Iterator, Mapping, Tuple
import functools
from datetime import timedelta

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
    return _get(uri, attempt)


@functools.cache
@modestly
def _get(uri: str, attempt: str):
    mprint(f"opening {uri} ({attempt})...")
    res = requests.get(uri)
    res.raise_for_status()
    return res.text


def _odds_page_uri(race: BoatRace, btype: BettingType) -> str:
    return (
        "https://www.boatrace.jp/owpc/pc/race/"
        f"odds{btype_to_code(btype)}?"
        f"rno={race.race_no}&jcd={race.cource:02}&hd={race.date}"
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
