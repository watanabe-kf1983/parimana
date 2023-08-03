from typing import Collection, Mapping

from parimana.base.eye import BettingType

_type_dict: Mapping[BettingType, str] = {
    BettingType.WIN: "1",
    BettingType.SHOW: "2",
    BettingType.EXACTA: "6",
    BettingType.QUINELLA: "4",
    BettingType.WIDE: "5",
    BettingType.TRIO: "7",
    BettingType.TRIFECTA: "8",
}
_type_dict_inv: Mapping[str, BettingType] = {v: k for k, v in _type_dict.items()}

supported_types: Collection[BettingType] = _type_dict.keys()


def btype_to_code(btype: BettingType) -> str:
    return _type_dict[btype]


def code_to_btype(code: str) -> BettingType:
    return _type_dict_inv[code]
