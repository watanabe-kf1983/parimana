from typing import Mapping

from bs4 import BeautifulSoup

from parimana.base.eye import BettingType, Eye
from parimana.netkeiba.base import code_to_btype, btype_to_code


def extract_odds(html: str, btype: BettingType) -> Mapping[Eye, float]:
    soup = BeautifulSoup(html.encode("utf-8"), "html.parser", from_encoding="utf-8")
    elements = soup.select(f"table td.Odds span[id^='odds-{btype_to_code(btype)}']")
    return {_elem_id_to_eye(e["id"]): float(e.get_text()) for e in elements}


def _elem_id_to_eye(id: str):
    _, btype_code, number = id.replace("_", "-").split("-")
    betting_type = code_to_btype(btype_code)
    names = [number[i : i + 2] for i in range(0, len(number), 2)]
    return Eye.from_names(names, betting_type)
