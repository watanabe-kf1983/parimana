from functools import cached_property
from typing import (
    Mapping,
    Sequence,
    Set,
    TypeVar,
)
from dataclasses import dataclass

from parimana.domain.base.eye import Eye
from parimana.domain.base.situation import Situation, Distribution, TripleDistribution

T = TypeVar("T")


@dataclass(frozen=True, order=True)
class Contestant:
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Contestants:
    contestants: Sequence[Contestant]

    @cached_property
    def contestants_map(self) -> Mapping[str, Contestant]:
        return {c.name: c for c in self.contestants}

    @cached_property
    def contestants_set(self) -> Set[Contestant]:
        return set(self.contestants)

    def _find_contestant(self, name) -> Contestant:
        if name in self.contestants_map:
            return self.contestants_map[name]
        else:
            raise ValueError(f"{name} Not Found in contestants")

    def situation(self, eye: Eye, frequency: float = 1) -> Situation[Contestant]:
        selected = eye.map(self._find_contestant)
        unselected = self.contestants_set - set(selected)
        return Situation.from_collections((selected, unselected), eye.text, frequency)

    def situation_by_step(
        self, eye: Eye, step_count: int, frequency: float = 1
    ) -> Situation[Contestant]:

        if eye.type.size < step_count:
            return Situation.from_collections(
                ((), (), self.contestants), eye.text, frequency
            )

        elif eye.type.sequencial:
            placed = eye.map(self._find_contestant)
            selected = placed[step_count : step_count + 1]
            ommitted = placed[:step_count]
            unselected = self.contestants_set - set(placed[: step_count + 1])
            return Situation.from_collections(
                (selected, unselected, ommitted), eye.text, frequency
            )

        else:
            return self.situation(eye, frequency=frequency)

    def destribution(
        self, vote_tallies: Mapping[Eye, float]
    ) -> Distribution[Contestant]:
        return Distribution([self.situation(k, v) for k, v in vote_tallies.items()])

    def triple_destribution(
        self, vote_tallies: Mapping[Eye, float]
    ) -> TripleDistribution[Contestant]:

        return TripleDistribution(
            *[
                Distribution(
                    [
                        self.situation_by_step(k, step, v)
                        for k, v in vote_tallies.items()
                    ]
                )
                for step in range(3)
            ]
        )

    @classmethod
    def from_names(cls, names: Sequence[str]) -> "Contestants":
        constrants = [Contestant(name) for name in names]
        return Contestants(constrants)

    @classmethod
    def no_absences(cls, number_of_contestants: int) -> "Contestants":
        digits = len(str(number_of_contestants))
        names = [f"{i:0{digits}}" for i in range(1, number_of_contestants + 1)]
        return Contestants.from_names(names)
