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
    frequency: float = 1

    @cached_property
    def constrants(self) -> Sequence[T]:
        return sorted(({r.a for r in self.relations} | {r.b for r in self.relations}))

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

    @classmethod
    def from_collections(
        cls, collections: Collection[Collection[T]], frequency: float = 1
    ) -> "Situation[T]":
        return Situation(sorted(iterate_relation(*collections)), frequency)


@dataclass(frozen=True)
class Distribution(Generic[T]):
    situations: Collection[Situation[T]]
