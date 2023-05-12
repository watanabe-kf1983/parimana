from typing import (
    Collection,
    Generic,
    Sequence,
    TypeVar,
)
from dataclasses import dataclass
from functools import cached_property

T = TypeVar("T")


@dataclass(frozen=True)
class RankCounter(Generic[T]):
    elements: Collection[T]

    @cached_property
    def rank_max(self) -> float:
        return len(self.elements) - 1

    @cached_property
    def rank_average(self) -> float:
        return self.rank_max / 2

    def rank(self, element: T) -> float:
        if isinstance(self.elements, Sequence):
            return self.rank_max - self.elements.index(element)
        else:
            return self.rank_average


@dataclass(frozen=True)
class MixedRankCounter(Generic[T]):
    superior: Collection[T]
    inferior: Collection[T]

    @cached_property
    def superior_rc(self) -> RankCounter[T]:
        return RankCounter(self.superior)

    @cached_property
    def inferior_rc(self) -> RankCounter[T]:
        return RankCounter(self.inferior)

    def rank(self, element: T) -> float:
        if element in self.superior_rc.elements:
            return self.superior_rc.rank(element) + self.inferior_rc.rank_max + 1
        else:
            return self.inferior_rc.rank(element)

    def rank_zero_ave(self, element: T) -> float:
        return self.rank(element) - self.rank_average

    @cached_property
    def rank_average(self) -> float:
        return (self.superior_rc.rank_max + self.inferior_rc.rank_max + 1) / 2
