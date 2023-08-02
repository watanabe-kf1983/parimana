from enum import Enum
from itertools import combinations, permutations, chain
from typing import Collection, Sequence, Callable, TypeVar
from dataclasses import dataclass
from functools import cached_property
import re

T = TypeVar("T")


class BettingType(Enum):
    WIN = (1, True, 1, 1, "red")
    PLACE = (2, False, 1, 2, "brown", "P")
    SHOW = (3, False, 1, 3, "olive", "S")
    EXACTA = (4, True, 2, 2, "magenta")
    QUINELLA = (5, False, 2, 2, "purple")
    WIDE = (6, False, 2, 3, "green", "W")
    TRIFECTA = (7, True, 3, 3, "orange")
    TRIO = (8, False, 3, 3, "blue")

    def __init__(
        self,
        id: int,
        sequencial: bool,
        size: int,
        place: int,
        color: str,
        prefix: str = "",
    ):
        self.id: int = id
        self.sequencial: bool = sequencial
        self.size: int = size
        self.place: int = place
        self.color: str = color
        self.prefix: str = prefix

    @classmethod
    def from_size_and_type(
        cls, sequencial: bool, size: int, place: int
    ) -> "BettingType":
        for bt in BettingType:
            if (sequencial == bt.sequencial) and size == bt.size and place == bt.place:
                return bt

        raise ValueError(f"{sequencial} {size} {place} type not exists.")

    @classmethod
    def from_prefix(cls, prefix: str) -> "BettingType":
        for bt in BettingType:
            if prefix == bt.prefix:
                return bt

        raise ValueError(f"prefix {prefix} type not exists.")


pattern = re.compile(r"(?P<prefix>[PSW]?)(?P<body>.*)")


@dataclass(frozen=True)
class Eye:
    text: str

    @cached_property
    def prefix(self) -> str:
        m = pattern.match(self.text)
        return m.group("prefix") if m else ""

    @cached_property
    def body(self) -> str:
        m = pattern.match(self.text)
        return m.group("body") if m else ""

    @cached_property
    def names(self) -> Collection[str]:
        name_list = re.split("[=-]", self.body)
        name_set = set(name_list)
        if not (len(name_list) == len(name_set)):
            raise ValueError(f"names duplicated: {name_list}")

        return name_set if self.prefix or ("=" in self.body) else name_list

    @cached_property
    def type(self) -> BettingType:
        if self.prefix:
            return BettingType.from_prefix(self.prefix)

        sequencial: bool = isinstance(self.names, Sequence)
        size: int = len(self.names)
        return BettingType.from_size_and_type(sequencial, size, size)

    def map(self, mapper: Callable[[str], T]) -> Collection[T]:
        if self.type.sequencial:
            return [mapper(n) for n in self.names]
        else:
            return {mapper(n) for n in self.names}

    def __str__(self):
        return self.text

    @classmethod
    def eyes_from_places(cls, places: Sequence[str]) -> Collection["Eye"]:
        return list(
            chain.from_iterable(cls.from_places(places, t) for t in BettingType)
        )

    @classmethod
    def all_eyes(cls, names: Sequence[str], t: BettingType) -> Sequence["Eye"]:
        if t.sequencial:
            return [cls.from_names(p, t) for p in permutations(names, t.size)]
        else:
            return [cls.from_names(p, t) for p in combinations(names, t.size)]

    @classmethod
    def from_names(cls, names: Sequence[str], t: BettingType) -> "Eye":
        won = names[: t.size]
        if t.sequencial:
            return Eye(t.prefix + "-".join(won))
        else:
            won = sorted(won)
            return Eye(t.prefix + "=".join(won))

    @classmethod
    def from_places(cls, places: Sequence[str], t: BettingType) -> Sequence["Eye"]:
        return [
            cls.from_names(names, t)
            for names in combinations(places[: t.place], t.size)
        ]
