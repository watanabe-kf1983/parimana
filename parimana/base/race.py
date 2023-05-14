from typing import (
    Sequence,
    TypeVar,
)
from dataclasses import dataclass, field


T = TypeVar("T")


@dataclass(frozen=True, order=True)
class Contestant:
    name: str

    def __str__(self) -> str:
        return self.name

    def match(self, name: str) -> bool:
        return self.name == name


@dataclass(frozen=True)
class Race:
    contestants: Sequence[Contestant] = field(repr=False, hash=False)
    name: str = ""

    def find_contestant(self, name) -> Contestant:
        matched = [c for c in self.contestants if c.match(name)]
        if matched:
            return matched[0]
        else:
            raise ValueError(f"{name} Not Found in contestants")

    @classmethod
    def no_absences(cls, number_of_contestants: int, name="") -> "Race":
        digits = len(str(number_of_contestants))
        constrants = [
            Contestant(f"{i:0{digits}}") for i in range(1, number_of_contestants + 1)
        ]
        return Race(constrants, name)


derby = Race.no_absences(18, "derby")
trial = Race.no_absences(6, "trial")
