from typing import Collection, Iterator, Mapping, Tuple
import functools

import requests

from parimana.base.eye import BettingType


def browse_odds_pages(
    date: str, cource: int, race_no: int, attempt: str
) -> Iterator[Tuple[str, BettingType]]:
    for btype in supported_types:
        page_content = _browse_odds_by_btype(date, cource, race_no, btype, attempt)
        yield (page_content, btype)


def _browse_odds_by_btype(
    date: str, cource: int, race_no: int, btype: BettingType, attempt: str
) -> Iterator[str]:
    uri = _odds_page_uri(date, cource, race_no, btype)
    return _get(uri, attempt)


@functools.cache
def _get(uri: str, attempt: str):
    print(f"opening {uri} ({attempt})...", end=" ", flush=True)
    res = requests.get(uri)
    res.raise_for_status()
    print("done.", flush=True)
    return res.text


def _odds_page_uri(date: str, cource: int, race_no: int, btype: BettingType) -> str:
    return (
        "https://www.boatrace.jp/owpc/pc/race/"
        f"odds{btype_to_code(btype)}?rno={race_no}&jcd={cource:02}&hd={date}"
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
