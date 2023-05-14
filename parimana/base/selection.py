from collections import defaultdict
from typing import (
    Collection,
    Generic,
    Mapping,
    TypeVar,
)
from dataclasses import dataclass
from functools import cached_property

from parimana.base.eye import Eye
from parimana.base.race import Race, Contestant
from parimana.base.superiority import Relation, Superiority, iterate_relation
from parimana.base.lang import Comparable

T = TypeVar("T", bound=Comparable)

# https://www.jra.go.jp/keiba/overseas/yougo/c10080_list.html

# pari-mutuel betting


@dataclass(frozen=True)
class Selection:
    race: Race
    eye: Eye

    @cached_property
    def relations(self) -> "Relations[Contestant]":
        selected = self.eye.map(self.race.find_contestant)
        unselected = set(self.race.contestants) - set(selected)
        relations = sorted(iterate_relation(selected, unselected))

        return Relations(relations, self.race.contestants)


@dataclass(frozen=True)
class Relations(Generic[T]):
    relations: Collection[Relation[T]]
    constrants: Collection[T]

    @cached_property
    def _relations_mapping(
        self,
    ) -> Mapping[T, Mapping[T, Superiority]]:
        data: dict[T, dict[T, Superiority]] = defaultdict(dict)
        for r in self.relations:
            data[r.a][r.b] = r.sa
            data[r.b][r.a] = r.sa.opposite

        return data

    @cached_property
    def _score_mapping(self) -> Mapping[T, int]:
        return {c: self._get_score(c) for c in self.constrants}

    def _get_score(self, e: T) -> int:
        return sum((v.score for _, v in self._relations_mapping[e].items()))

    def get_score(self, e: T) -> int:
        return self._score_mapping[e]

    def get_superiority(self, a: T, b: T) -> Superiority:
        return self._relations_mapping[a][b]
