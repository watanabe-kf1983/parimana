from typing import Mapping

from bs4 import BeautifulSoup
import numpy as np

from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds


names = [str(n) for n in range(1, 7)]
trifecta_eyes = Eye.all_eyes(names, BettingType.TRIFECTA)


def extract_odds(html: str, btype: BettingType) -> Mapping[Eye, float]:
    if btype == BettingType.TRIFECTA:
        return extract_odds_trifecta(html)
    else:
        return {}


def extract_odds_trifecta(html: str) -> Mapping[Eye, float]:
    soup = BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")
    table = soup.select_one("div.contentsFrame1_inner > div:nth-child(7) > table")
    extracted = [Odds.from_text(e.get_text()) for e in table.select("td.oddsPoint")]
    odds_list = list(np.array(extracted).reshape(20, 6).T.reshape(-1))
    return {eye: odds for eye, odds in zip(trifecta_eyes, odds_list)}
