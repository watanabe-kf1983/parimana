from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, Mapping, Sequence, Tuple, TypeVar

from parimana.base import (
    BettingType,
    Comparable,
    Distribution,
    RaceOddsPool,
    RaceSource,
)
from parimana.analyse.analysis_result import AnalysisResult
from parimana.analyse.regression import RegressionModel
from parimana.analyse.correlation import (
    cor_mapping_to_sr,
)
from parimana.analyse.win_rate import extract_win_rate, df_from_win_rate
from parimana.analyse.ability import (
    estimate_ability_map,
    find_uncertainty_map,
)
from parimana.analyse.mvn_model import MvnModel
from parimana.analyse.odds_eval import (
    calc_vote_tally,
)


T = TypeVar("T", bound=Comparable)


class Analyser(ABC, Generic[T]):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def analyse(
        self,
        odds_pool: RaceOddsPool,
        simulation_count: int,
        odds_model: Mapping[BettingType, RegressionModel] = {},
    ) -> AnalysisResult[T]:
        pass


@dataclass(frozen=True)
class OnePassAnalyser(Analyser[T]):
    _name: str
    cor_extractor: Callable[[Distribution[T]], Mapping[Tuple[T, T], float]]

    @property
    def name(self) -> str:
        return self._name

    def analyse(
        self,
        odds_pool: RaceOddsPool,
        simulation_count: int,
        odds_model: Mapping[BettingType, RegressionModel] = {},
    ) -> AnalysisResult[T]:
        print(f"extract_destribution by '{self.name}' ...")
        vote_tallies = calc_vote_tally(odds_pool.odds, odds_pool.vote_ratio, odds_model)
        dist = odds_pool.contestants.destribution(vote_tallies)
        print(f"estimating model by '{self.name}' ...")
        model = self.estimate_model(dist)
        print(f"simulating '{model.name}' ...")
        chances = model.simulate(simulation_count)
        return AnalysisResult(odds_pool, model, chances)

    def estimate_model(self, dist: Distribution[T]) -> MvnModel[T]:
        win_rates = extract_win_rate(dist.relations, dist.members)
        wr_df = df_from_win_rate(win_rates)
        cor = self.cor_extractor(dist)
        cor_sr = cor_mapping_to_sr(cor)
        corwr_df = cor_sr.to_frame().join(wr_df)
        u_map = find_uncertainty_map(corwr_df)
        a_map = estimate_ability_map(corwr_df, u_map)
        return MvnModel(cor_sr, u_map, a_map, dist.members, self.name)


@dataclass(frozen=True)
class MultiPassAnalyser(Analyser[T]):
    _name: str
    analysers: Sequence[Analyser[T]]

    @property
    def name(self) -> str:
        return self._name

    def analyse(
        self,
        race: RaceSource,
        simulation_count: int,
        odds_model: Mapping[BettingType, RegressionModel] = {},
    ) -> AnalysisResult[T]:
        om = odds_model
        for a in self.analysers:
            result = a.analyse(race, simulation_count, om)
            om = result.odds_chance.regression_model

        result.model.name = self.name
        return result
