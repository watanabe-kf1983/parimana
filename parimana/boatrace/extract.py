from typing import Mapping, Sequence

from bs4 import BeautifulSoup, Tag
import numpy as np

from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds


# trifecta_eyes = Eye.all_eyes(names, BettingType.TRIFECTA)
# wide_eyes = Eye.all_eyes(names, BettingType.WIDE)
# trio_eyes = Eye.all_eyes(names, BettingType.TRIO)


def extract_odds(html: str, btype: BettingType) -> Mapping[Eye, Odds]:
    soup = BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")
    table = select_table(btype, soup)
    extracted = extract_odds_from_table(table)
    eyes = eyes_table_order(btype)
    return {eye: odds for eye, odds in zip(eyes, extracted)}


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


def extract_odds_from_table(table: Tag) -> Sequence[Odds]:
    return [Odds.from_text(e.get_text()) for e in table.select("td.oddsPoint")]


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
