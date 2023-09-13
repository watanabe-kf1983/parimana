from abc import ABC, abstractmethod
from typing import Optional


class Race(ABC):
    @property
    @abstractmethod
    def race_id(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_id(cls, race_id: str) -> Optional["Race"]:
        pass
