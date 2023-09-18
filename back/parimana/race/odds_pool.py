from dataclasses import dataclass
from datetime import datetime
from functools import total_ordering
from typing import Optional

from parimana.base import OddsPool
from parimana.race.race import Race


@total_ordering
@dataclass
class OddsTimeStamp:
    update_time: Optional[datetime] = None

    def __str__(self) -> str:
        return (
            "Confirmed"
            if self.update_time is None
            else self.update_time.strftime("%Y%m%d%H%M")
        )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.update_time == other.update_time

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.is_confirmed:
            return False
        elif other.is_confirmed:
            return True
        else:
            return self.update_time < other.update_time

    @property
    def is_confirmed(self) -> bool:
        return not bool(self.update_time)

    @classmethod
    def confirmed(cls) -> "OddsTimeStamp":
        return OddsTimeStamp(None)


@dataclass
class RaceOddsPool(OddsPool):
    race: Race
    timestamp: OddsTimeStamp

    @property
    def key(self) -> str:
        return f"{self.race.race_id}/{self.timestamp}"


class OddsUpdatedException(Exception):
    pass
