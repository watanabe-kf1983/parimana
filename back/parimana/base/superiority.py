from enum import Enum
from functools import cached_property
from typing import (
    Collection,
    Generic,
    Iterable,
    Sequence,
    TypeVar,
)
from dataclasses import dataclass
import itertools

from parimana.base.compare import Comparable

T = TypeVar("T", bound=Comparable)


class Superiority(Enum):
    SUPERIOR = (1, ">")
    UNKNOWN = (0, "?")
    EQUALS = (0, "=")
    INFERIOR = (-1, "<")

    def __init__(self, score: int, sign: str):
        self.score: int = score
        self.sign: str = sign

    @cached_property
    def opposite(self):
        if self == Superiority.INFERIOR:
            return Superiority.SUPERIOR
        elif self == Superiority.SUPERIOR:
            return Superiority.INFERIOR
        else:
            return self


@dataclass(frozen=True, order=True)
class Relation(Generic[T]):
    a: T
    b: T
    sa: Superiority

    def __post_init__(self):
        if self.a == self.b and not self.sa == Superiority.EQUALS:
            raise ValueError(f"a equals b but not equal:{self.a} {self.b} {self.sa}")

    @cached_property
    def record(self):
        return {"a": str(self.a), "b": str(self.b), "sa": self.sa.name}

    def __str__(self) -> str:
        return f"{self.a}{self.sa.sign}{self.b}"


def _iterate_relation_single(col: Collection[T]) -> Iterable[Relation[T]]:
    if isinstance(col, Sequence):
        sp = Superiority.SUPERIOR
    else:
        sp = Superiority.UNKNOWN
    i1 = (Relation(a, b, sp) for (a, b) in itertools.combinations(col, 2))
    i2 = (Relation(b, a, sp.opposite) for (a, b) in itertools.combinations(col, 2))
    i3 = (Relation(a, a, Superiority.EQUALS) for a in col)
    return itertools.chain(i1, i2, i3)


def iterate_relation(*collections: Sequence[T]) -> Iterable[Relation[T]]:
    i1 = (
        Relation(a, b, Superiority.SUPERIOR)
        for (col_a, col_b) in itertools.combinations(collections, 2)
        for a, b in itertools.product(col_a, col_b)
    )
    i2 = (
        Relation(b, a, Superiority.INFERIOR)
        for (col_a, col_b) in itertools.combinations(collections, 2)
        for a, b in itertools.product(col_a, col_b)
    )
    i3 = itertools.chain.from_iterable(
        (_iterate_relation_single(col) for col in collections)
    )
    return itertools.chain(i1, i2, i3)
