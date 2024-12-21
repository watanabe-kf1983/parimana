from typing import Collection, Iterator, Mapping, Tuple
from datetime import timedelta, datetime

from parimana.domain.base import BettingType
from parimana.external.scraping_utils.modest import ModestFunction
from parimana.external.boatrace.base import BoatRace
import parimana.external.boatrace.browser as browser


modestly = ModestFunction(interval=timedelta(seconds=1.5))


def get_source_uri(race: BoatRace) -> str:
    return _odds_page_uri(race, BettingType.TRIFECTA)


def browse_for_timestamp(race: BoatRace) -> str:
    return browse_odds_page(race, BettingType.WIN)


def browse_odds_pages(
    race: BoatRace, attempt: str
) -> Iterator[Tuple[str, BettingType]]:
    for btype in supported_types:
        page_content = browse_odds_page(race, btype, attempt)
        yield (page_content, btype)


def browse_odds_page(race: BoatRace, btype: BettingType, attempt: str = "1st") -> str:
    uri = _odds_page_uri(race, btype)
    return browser.get(uri, f"{datetime.now():%Y%m%d%H%M}-{attempt}")


def _odds_page_uri(race: BoatRace, btype: BettingType) -> str:
    return (
        f"https://www.boatrace.jp/owpc/pc/race/odds{btype_to_code(btype)}?"
        f"rno={race.race_no}&jcd={race.jo_code}&hd={race.date:%Y%m%d}"
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
