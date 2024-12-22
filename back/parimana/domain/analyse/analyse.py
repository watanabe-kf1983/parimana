from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Mapping, Sequence, Tuple

from parimana.io.message import mprint
from parimana.domain.base import BettingType, Distribution, OddsPool, Contestant
from parimana.domain.analyse.analysis_result import AnalysisResult
from parimana.domain.analyse.regression import RegressionModel
from parimana.domain.analyse.correlation import (
    cor_mapping_to_sr,
)
from parimana.domain.analyse.win_rate import extract_win_rate, df_from_win_rate
from parimana.domain.analyse.ability import (
    estimate_ability_map,
    find_uncertainty_map,
)
from parimana.domain.analyse.mvn_model import MvnModel
from parimana.domain.analyse.odds_eval import (
    calc_vote_tally,
)


class Analyser(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def analyse(
        self,
        odds_pool: OddsPool,
        simulation_count: int,
        odds_model: Mapping[BettingType, RegressionModel] = {},
    ) -> AnalysisResult:
        pass


@dataclass(frozen=True)
class OnePassAnalyser(Analyser):
    _name: str
    cor_extractor: Callable[
        [Distribution[Contestant]], Mapping[Tuple[Contestant, Contestant], float]
    ]

    @property
    def name(self) -> str:
        return self._name

    def analyse(
        self,
        odds_pool: OddsPool,
        simulation_count: int,
        odds_model: Mapping[BettingType, RegressionModel] = {},
    ) -> AnalysisResult:
        mprint(f"extract_destribution by '{self.name}' ...")
        vote_tallies = calc_vote_tally(odds_pool.odds, odds_pool.vote_ratio, odds_model)
        dist = odds_pool.contestants.destribution(vote_tallies)
        mprint(f"estimating model by '{self.name}' ...")
        model = self.estimate_model(dist)
        mprint(f"simulating '{model.name}' ...")
        chances = model.simulate(simulation_count)
        return AnalysisResult(odds_pool, model, chances)

    def estimate_model(self, dist: Distribution[Contestant]) -> MvnModel[Contestant]:
        win_rates = extract_win_rate(dist.relations, dist.members)
        wr_df = df_from_win_rate(win_rates)
        cor = self.cor_extractor(dist)
        cor_sr = cor_mapping_to_sr(cor)
        corwr_df = cor_sr.to_frame().join(wr_df)
        u_map = find_uncertainty_map(corwr_df)
        a_map = estimate_ability_map(corwr_df, u_map)
        return MvnModel(cor_sr, u_map, a_map, dist.members, self.name)


@dataclass(frozen=True)
class MultiPassAnalyser(Analyser):
    _name: str
    analysers: Sequence[Analyser]

    @property
    def name(self) -> str:
        return self._name

    def analyse(
        self,
        odds_pool: OddsPool,
        simulation_count: int,
        odds_model: Mapping[BettingType, RegressionModel] = {},
    ) -> AnalysisResult:
        om = odds_model
        for a in self.analysers:
            result = a.analyse(odds_pool, simulation_count, om)
            om = result.eev.regression_model

        result.model.name = self.name
        return result
