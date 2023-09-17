from dataclasses import dataclass
from datetime import datetime
from functools import total_ordering
from typing import Mapping, Optional

from parimana.base.contestants import Contestants
from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds
from parimana.base.race import Race


@total_ordering
@dataclass
class OddsTimeStamp:
    update_time: Optional[datetime] = None

    def __str__(self) -> str:
        return (
            "Confirmed"
            if self.is_confirmed
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
    @property
    def confirmed(cls) -> "OddsTimeStamp":
        return OddsTimeStamp(None)


@dataclass
class RaceOddsPool:
    race: Race
    odds: Mapping[Eye, Odds]
    timestamp: OddsTimeStamp
    vote_ratio: Mapping[BettingType, float]

    @property
    def contestants(self) -> Contestants:
        names = [eye.text for eye in self.odds.keys() if eye.type == BettingType.WIN]
        return Contestants.from_names(names)

    @property
    def key(self) -> str:
        return f"{self.race.race_id}/{self.timestamp}"


class OddsUpdatedException(Exception):
    pass
