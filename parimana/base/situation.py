from collections import defaultdict
from functools import cached_property
from typing import (
    Collection,
    Generic,
    Mapping,
    Sequence,
    Tuple,
    TypeVar,
)
from dataclasses import dataclass

from parimana.base.compare import Comparable
from parimana.base.superiority import Superiority, Relation, iterate_relation

T = TypeVar("T", bound=Comparable)


@dataclass(frozen=True)
class Situation(Generic[T]):
    relations: Collection[Relation[T]]
    name: str = ""
    frequency: float = 1
    accuracy: int = 1

    @cached_property
    def members(self) -> Sequence[T]:
        return sorted({r.a for r in self.relations})

    @cached_property
    def superiorities(
        self,
    ) -> Mapping[T, Mapping[T, Superiority]]:
        data: dict[T, dict[T, Superiority]] = defaultdict(dict)
        for r in self.relations:
            data[r.a][r.b] = r.sa
        return data

    @cached_property
    def scores(self) -> Mapping[T, int]:
        return {c: self._calc_score(c) for c in self.members}

    def _calc_score(self, e: T) -> int:
        return sum((v.score for _, v in self.superiorities[e].items()))

    def _get_score(self, e: T) -> int:
        return self.scores[e]

    def _calc_score_exclude(self, e: T, exclude: T) -> int:
        return self._get_score(e) - self.get_superiority(e, exclude).score

    @cached_property
    def scores_matrix(self) -> Mapping[Tuple[T, T], Tuple[int, int]]:
        return {
            (a, b): (self._calc_score_exclude(a, b), self._calc_score_exclude(b, a))
            for a in self.members
            for b in self.members
        }

    def get_superiority(self, a: T, b: T) -> Superiority:
        return self.superiorities[a][b]

    @classmethod
    def from_collections(
        cls,
        collections: Sequence[Collection[T]],
        name: str = "",
        frequency: float = 1,
    ) -> "Situation[T]":
        return Situation(
            sorted(iterate_relation(*collections)), name, frequency, len(collections[0])
        )


@dataclass(frozen=True)
class Distribution(Generic[T]):
    situations: Sequence[Situation[T]]

    @cached_property
    def members(self) -> Sequence[T]:
        return next(iter(self.situations)).members

    @cached_property
    def scores(self) -> Collection[Tuple[Situation[T], Mapping[T, int]]]:
        return [(s, s.scores) for s in self.situations]

    @cached_property
    def scores_matrix(
        self,
    ) -> Collection[Tuple[Situation[T], Mapping[Tuple[T, T], Tuple[int, int]]]]:
        return [(s, s.scores_matrix) for s in self.situations]

    @cached_property
    def relations(
        self,
    ) -> Collection[Tuple[Situation[T], Collection[Relation[T]]]]:
        return [(s, s.relations) for s in self.situations]
