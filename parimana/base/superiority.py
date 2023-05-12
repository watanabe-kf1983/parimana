# from enum import Enum
from typing import (
    Collection,
    Generic,
    Iterable,
    Iterator,
    Sequence,
    Tuple,
    TypeVar,
)
from dataclasses import dataclass
import itertools

T = TypeVar("T")


def iterate_inside_col(col: Collection[T]) -> Iterable[Tuple[T, T]]:
    return itertools.combinations(col, 2) if isinstance(col, Sequence) else []


@dataclass(frozen=True)
class SuperiorityRelation(Generic[T]):
    superior: T
    inferior: T

    def __str__(self) -> str:
        return f"{self.superior}>{self.inferior}"


@dataclass(frozen=True)
class RelationIterator(Generic[T]):
    superiors: Collection[T]
    inferiors: Collection[T]

    def iterator(self) -> Iterator[SuperiorityRelation[T]]:
        r1 = itertools.product(self.superiors, self.inferiors)
        r2 = iterate_inside_col(self.superiors)
        r3 = iterate_inside_col(self.inferiors)
        return (SuperiorityRelation(s, i) for (s, i) in itertools.chain(r1, r2, r3))
