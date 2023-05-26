from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Collection, Generic, TypeVar
from parimana.situation.situation import Comparable
from parimana.vote.eye import Eye


T = TypeVar("T", bound=Comparable)


@dataclass(frozen=True)
class Results:
    eye: Eye
    frequency: float


class Model(ABC, Generic[T]):
    @abstractmethod
    def simulate(self, n: float) -> Collection[Results]:
        pass
