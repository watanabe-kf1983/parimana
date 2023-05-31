from typing import Iterator, Tuple

import requests

from parimana.base.eye import BettingType
from parimana.boatrace.base import btype_to_code


def browse_odds_pages(
    date: str, cource: int, number: int
) -> Iterator[Tuple[str, BettingType]]:
    for btype in [BettingType.TRIFECTA]:
        for page_content in _browse_odds_by_btype(date, cource, number, btype):
            yield (page_content, btype)


def _browse_odds_by_btype(
    date: str, cource: int, number: int, btype: BettingType
) -> Iterator[str]:
    uri = _odds_page_uri(date, cource, number, btype)
    print(f"opening {uri} ...", end=" ", flush=True)
    res = requests.get(uri)
    print("done.", flush=True)
    res.raise_for_status()
    yield res.text
    res.close()


def _odds_page_uri(date: str, cource: int, number: int, btype: BettingType) -> str:
    return (
        "https://www.boatrace.jp/owpc/pc/race/"
        f"odds{btype_to_code(btype)}?rno={number}&jcd={cource:02}&hd={date}"
    )
