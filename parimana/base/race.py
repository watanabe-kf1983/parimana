from abc import ABC, abstractmethod
from functools import cached_property
from pathlib import Path
import pickle
from typing import Mapping, Optional
from parimana.base.contestants import Contestants


from parimana.base.eye import BettingType, Eye
from parimana.base.odds import Odds


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
    def collect_odds(self) -> Mapping[Eye, Odds]:
        pass

    @classmethod
    @abstractmethod
    def from_race_id(cls, race_id: str) -> Optional["Race"]:
        pass

    @cached_property
    def base_dir(self) -> Path:
        dir = Path(".output") / self.race_id
        dir.mkdir(exist_ok=True, parents=True)
        return dir

    @cached_property
    def odds_cache_path(self) -> Path:
        return self.base_dir / "odds.pickle"

    def remove_odds_cache(self) -> None:
        self.odds_cache_path.unlink(missing_ok=True)
        if hasattr(self, "odds"):
            delattr(self, "odds")

    @cached_property
    def odds(self) -> Mapping[Eye, Odds]:
        return self._get_odds()

    def _get_odds(self) -> Mapping[Eye, Odds]:
        odds_p_path = self.odds_cache_path
        if not odds_p_path.exists():
            print("collecting odds...")
            odds = self.collect_odds()
            print(f"writing odds to {odds_p_path}...")
            with open(odds_p_path, "wb") as f:
                pickle.dump(odds, f)

        else:
            print(f"reading odds from {odds_p_path}...")
            with open(odds_p_path, "rb") as f:
                odds = pickle.load(f)

        return odds
