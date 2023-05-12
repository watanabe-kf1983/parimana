from typing import Collection, Sequence, Callable, TypeVar
from dataclasses import dataclass
from functools import cached_property
import re

T = TypeVar("T")


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
    def is_sequencial(self) -> bool:
        return isinstance(self.names, Sequence)

    @cached_property
    def type(self) -> str:
        if self.is_sequencial:
            return {1: "WIN", 2: "EXACTA", 3: "TRIFECTA"}[len(self.names)]
        else:
            return {2: "QUINELLA", 3: "TRIO"}[len(self.names)]

    def map(self, mapper: Callable[[str], T]) -> Collection[T]:
        if self.is_sequencial:
            return [mapper(n) for n in self.names]
        else:
            return {mapper(n) for n in self.names}

    def __str__(self):
        return f"{self.type} {self.text}"
