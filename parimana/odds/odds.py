# from enum import Enum
from typing import (
    Collection,
    Mapping,
    Set,
    TypeVar,
)
from dataclasses import dataclass
from functools import cached_property

from parimana.base.selection import Selection
from parimana.base.race import Race, Contestant
from parimana.base.superiority import SuperiorityRelation, RelationIterator

T = TypeVar("T")

# https://www.jra.go.jp/keiba/overseas/yougo/c10080_list.html

# pari-mutuel betting


@dataclass(frozen=True)
class Betting:
    weight: int
    selection: Selection


@dataclass(frozen=True)
class RaceBettings:
    race: Race
    selections: Collection[Betting]

