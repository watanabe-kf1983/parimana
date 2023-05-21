from collections import defaultdict
from functools import cached_property
from typing import (
    Collection,
    Generic,
    Mapping,
    Sequence,
    TypeVar,
)
from dataclasses import dataclass

from parimana.situation.compare import Comparable
from parimana.situation.superiority import Superiority, Relation, iterate_relation

T = TypeVar("T", bound=Comparable)


@dataclass(frozen=True)
class Situation(Generic[T]):
    relations: Collection[Relation[T]]
    name: str = ""
    frequency: float = 1

    @cached_property
    def members(self) -> Sequence[T]:
        return sorted(({r.a for r in self.relations} | {r.b for r in self.relations}))

    @cached_property
    def superiorities(
        self,
    ) -> Mapping[T, Mapping[T, Superiority]]:
        data: dict[T, dict[T, Superiority]] = defaultdict(dict)
        for r in self.relations:
            data[r.a][r.b] = r.sa
            data[r.b][r.a] = r.sa.opposite

        return data

    @cached_property
    def scores(self) -> Mapping[T, int]:
        return {c: self._calc_score(c) for c in self.members}

    def _calc_score(self, e: T) -> int:
        return sum((v.score for _, v in self.superiorities[e].items()))

    def get_score(self, e: T) -> int:
        return self.scores[e]

    def get_score_exclude(self, e: T, exclude: T) -> int:
        return self.get_score(e) - self.get_superiority(e, exclude).score

    def get_superiority(self, a: T, b: T) -> Superiority:
        return self.superiorities[a][b]

    @classmethod
    def from_collections(
        cls,
        collections: Collection[Collection[T]],
        name: str = "",
        frequency: float = 1,
    ) -> "Situation[T]":
        return Situation(sorted(iterate_relation(*collections)), name, frequency)


@dataclass(frozen=True)
class Distribution(Generic[T]):
    situations: Sequence[Situation[T]]
