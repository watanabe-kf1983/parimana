# from enum import Enum
from typing import (
    Collection,
    Mapping,
    Set,
    TypeVar,
)
from dataclasses import dataclass
from functools import cached_property

from parimana.base.eye import Eye
from parimana.base.rank import MixedRankCounter
from parimana.base.race import Race, Contestant
from parimana.base.superiority import SuperiorityRelation, RelationIterator

T = TypeVar("T")

# https://www.jra.go.jp/keiba/overseas/yougo/c10080_list.html

# pari-mutuel betting


@dataclass(frozen=True)
class Selection:
    race: Race
    eye: Eye

    @cached_property
    def selection(self) -> Collection[Contestant]:
        return self.eye.map(self.race.find_contestant)

    @cached_property
    def selected(self) -> Collection[Contestant]:
        return self.selection

    @cached_property
    def unselected(self) -> Collection[Contestant]:
        return set(self.race.constrants) - set(self.selected)

    @cached_property
    def rcounter(self) -> MixedRankCounter:
        return MixedRankCounter(self.selected, set(self.unselected))

    def rank(self, contestant: Contestant) -> float:
        return self.rcounter.rank_zero_ave(contestant)

    @cached_property
    def rank_dict(self) -> Mapping[Contestant, float]:
        return {c: self.rank(c) for c in self.race.constrants}

    @cached_property
    def relations(self) -> Set[SuperiorityRelation[Contestant]]:
        return set(RelationIterator(self.selected, self.unselected).iterator())

    def print_place(self) -> None:
        for txt in sorted(f"{k}: {v}" for k, v in self.rank_dict.items()):
            print(txt)

    def print_relations(self) -> None:
        for txt in sorted(str(r) for r in self.relations):
            print(txt)

    @classmethod
    def from_text(cls, race: Race, eye_text: str) -> "Selection":
        return Selection(race, Eye(eye_text))
