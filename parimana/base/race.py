from abc import ABC, abstractmethod
from functools import cached_property
from pathlib import Path
import pickle
from typing import Mapping
from parimana.base.contestants import Contestant, Contestants


from parimana.base.eye import BettingType, Eye
from parimana.base.situation import Distribution


class Race(ABC):
    @property
    @abstractmethod
    def contestants(self) -> Contestants:
        pass

    @property
    @abstractmethod
    def vote_ratio(self) -> Mapping[BettingType, float]:
        pass

    @property
    @abstractmethod
    def vote_tally_total(self) -> float:
        pass

    @property
    @abstractmethod
    def race_id(self) -> str:
        pass

    @abstractmethod
    def collect_odds(self) -> Mapping[Eye, float]:
        pass

    @cached_property
    def base_dir(self) -> Path:
        dir = Path(".output") / self.race_id
        dir.mkdir(exist_ok=True, parents=True)
        return dir

    @cached_property
    def odds(self) -> Mapping[Eye, float]:
        return self.get_odds()

    def get_odds(self, recollect_odds: bool = False) -> Mapping[Eye, float]:
        odds_p_path = self.base_dir / "odds.pickle"
        if recollect_odds or not odds_p_path.exists():
            odds = self.collect_odds()
            with open(odds_p_path, "wb") as f:
                pickle.dump(odds, f)

        with open(odds_p_path, "rb") as f:
            odds = pickle.load(f)

        return odds

    def destribution(self, recollect_odds: bool = False) -> Distribution[Contestant]:
        odds = self.get_odds(recollect_odds)
        return self.contestants.destribution_from_odds(
            odds=odds,
            vote_ratio=self.vote_ratio,
            vote_tally_total=self.vote_tally_total,
        )
