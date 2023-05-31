from typing import Mapping

from parimana.base.eye import BettingType

_type_dict: Mapping[BettingType, str] = {
    BettingType.TRIO: "3f",
    BettingType.TRIFECTA: "3t",
}
_type_dict_inv: Mapping[str, BettingType] = {v: k for k, v in _type_dict.items()}


def btype_to_code(btype: BettingType) -> str:
    return _type_dict[btype]


def code_to_btype(code: str) -> BettingType:
    return _type_dict_inv[code]
