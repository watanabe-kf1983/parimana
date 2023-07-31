from typing import Mapping, Sequence

from bs4 import BeautifulSoup, Tag
import numpy as np

from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds


names = [str(n) for n in range(1, 7)]
trifecta_eyes = Eye.all_eyes(names, BettingType.TRIFECTA)
wide_eyes = Eye.all_eyes(names, BettingType.WIDE)


def extract_odds(html: str, btype: BettingType) -> Mapping[Eye, Odds]:
    soup = BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")
    if btype == BettingType.TRIFECTA:
        return extract_odds_trifecta(soup)
    elif btype == BettingType.WIDE:
        return extract_odds_wide(soup)
    else:
        return {}


def extract_odds_trifecta(soup: BeautifulSoup) -> Mapping[Eye, Odds]:
    table = select_first_table(soup)
    extracted = extract_odds_from_table(table)
    odds_list = list(np.array(extracted).reshape(20, 6).T.reshape(-1))
    return {eye: odds for eye, odds in zip(trifecta_eyes, odds_list)}


def extract_odds_wide(soup: BeautifulSoup) -> Mapping[Eye, Odds]:
    table = select_first_table(soup)
    extracted = extract_odds_from_table(table)
    eyes = sorted(wide_eyes, key=lambda e: sorted(e.names)[1])
    return {eye: odds for eye, odds in zip(eyes, extracted)}


def select_first_table(soup: BeautifulSoup) -> Tag:
    return soup.select_one("div.contentsFrame1_inner > div:nth-child(7) > table")


def extract_odds_from_table(table: Tag) -> Sequence[Odds]:
    return [Odds.from_text(e.get_text()) for e in table.select("td.oddsPoint")]
