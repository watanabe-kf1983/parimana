from typing import Collection, Iterator, Mapping, Tuple
import functools

import requests

from parimana.base import BettingType
from parimana.races.boatrace.race import BoatRace


def browse_odds_pages(
    race: BoatRace, attempt: str
) -> Iterator[Tuple[str, BettingType]]:
    for btype in supported_types:
        page_content = _browse_odds_by_btype(race, btype, attempt)
        yield (page_content, btype)


def _browse_odds_by_btype(
    race: BoatRace, btype: BettingType, attempt: str
) -> Iterator[str]:
    uri = _odds_page_uri(race, btype)
    return _get(uri, attempt)


@functools.cache
def _get(uri: str, attempt: str):
    print(f"opening {uri} ({attempt})...", end=" ", flush=True)
    res = requests.get(uri)
    res.raise_for_status()
    print("done.", flush=True)
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
