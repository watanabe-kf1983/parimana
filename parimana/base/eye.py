from enum import Enum
from typing import Collection, Sequence, Callable, TypeVar
from dataclasses import dataclass
from functools import cached_property
import re

T = TypeVar("T")


class BettingType(Enum):
    WIN = (True, 1)
    EXACTA = (True, 2)
    TRIFECTA = (True, 3)
    QUINELLA = (False, 2)
    TRIO = (False, 3)

    def __init__(self, sequencial: bool, size: int):
        self.sequencial: bool = sequencial
        self.size: int = size


@dataclass(frozen=True)
class Eye:
    text: str

    @cached_property
    def names(self) -> Collection[str]:
        name_list = re.split("[=-]", self.text)
        name_set = set(name_list)
        if not (len(name_list) == len(name_set)):
            raise ValueError(f"names duplicated: {name_list}")

        return name_set if "=" in self.text else name_list

    @cached_property
    def type(self) -> BettingType:
        sequencial: bool = isinstance(self.names, Sequence)
        size: int = len(self.names)
        return BettingType((sequencial, size))  # type: ignore

    @cached_property
    def record(self):
        return {"eye": self.text, "type": self.type.name}

    def map(self, mapper: Callable[[str], T]) -> Collection[T]:
        if self.type.sequencial:
            return [mapper(n) for n in self.names]
        else:
            return {mapper(n) for n in self.names}

    @classmethod
    def from_record(cls, rec):
        return Eye(rec["eye"])

    def __str__(self):
        return self.text
