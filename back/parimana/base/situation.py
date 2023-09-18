from collections import defaultdict
from functools import cache, cached_property
from typing import (
    Collection,
    Generic,
    Mapping,
    Sequence,
    Tuple,
    TypeVar,
)
from dataclasses import dataclass

import scipy.stats

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
    def members_size(self) -> int:
        return len(self.members)

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

    @cached_property
    def scores_matrix(self) -> Mapping[Tuple[T, T], Tuple[int, int]]:
        return {
            (a, b): (self._calc_score_exclude(a, b), self._calc_score_exclude(b, a))
            for a in self.members
            for b in self.members
        }

    @cached_property
    def ppfs(self) -> Mapping[T, float]:
        return {c: self._calc_ppf(c) for c in self.members}

    @cached_property
    def ppfs_matrix(self) -> Mapping[Tuple[T, T], Tuple[float, float]]:
        return {
            (a, b): (self._calc_ppf_exclude(a, b), self._calc_ppf_exclude(b, a))
            for a in self.members
            for b in self.members
        }

    def _calc_score(self, e: T) -> int:
        return sum((v.score for _, v in self.superiorities[e].items()))

    def _get_score(self, e: T) -> int:
        return self.scores[e]

    def _calc_ppf(self, e: T) -> float:
        score = self._get_score(e)
        return ppf_by_score(self.members_size, score)

    def _calc_score_exclude(self, e: T, exclude: T) -> int:
        return self._get_score(e) - self.get_superiority(e, exclude).score

    def _calc_ppf_exclude(self, e: T, exclude: T) -> float:
        m_size = self.members_size if e == exclude else self.members_size - 1
        score = self._calc_score_exclude(e, exclude)
        return ppf_by_score(m_size, score)

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


@cache
def pp_by_score(num_of_member: int, score: int) -> float:
    return (1 - score / num_of_member) / 2


@cache
def ppf_by_score(num_of_member: int, score: int) -> float:
    q = pp_by_score(num_of_member, score)
    return scipy.stats.norm.ppf(q, loc=0, scale=1)


@dataclass(frozen=True)
class Distribution(Generic[T]):
    situations: Sequence[Situation[T]]

    @cached_property
    def members(self) -> Sequence[T]:
        return next(iter(self.situations)).members

    @cached_property
    def scores(self) -> Collection[Tuple[Situation[T], Mapping[T, float]]]:
        return [(s, s.scores) for s in self.situations]

    @cached_property
    def scores_matrix(
        self,
    ) -> Collection[Tuple[Situation[T], Mapping[Tuple[T, T], Tuple[float, float]]]]:
        return [(s, s.scores_matrix) for s in self.situations]

    @cached_property
    def ppf(self) -> Collection[Tuple[Situation[T], Mapping[T, float]]]:
        return [(s, s.ppfs) for s in self.situations]

    @cached_property
    def ppf_matrix(
        self,
    ) -> Collection[Tuple[Situation[T], Mapping[Tuple[T, T], Tuple[float, float]]]]:
        return [(s, s.ppfs_matrix) for s in self.situations]

    @cached_property
    def relations(
        self,
    ) -> Collection[Tuple[Situation[T], Collection[Relation[T]]]]:
        return [(s, s.relations) for s in self.situations]
