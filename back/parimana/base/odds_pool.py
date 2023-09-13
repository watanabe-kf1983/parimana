from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Optional

from parimana.base.contestants import Contestants
from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds
from parimana.base.race import Race


@dataclass
class OddsTimeStamp:
    update_time: Optional[datetime] = None

    def __str__(self) -> str:
        return (
            "Confirmed"
            if self.is_confirmed
            else self.update_time.strftime("%Y%m%d%H%M")
        )

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


class OddsUpdatedException(Exception):
    pass
