from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Callable, Generic, Mapping, Sequence, Tuple, TypeVar

import pandas as pd

from parimana.base.eye import BettingType, Eye
from parimana.base.situation import Comparable, Distribution
from parimana.base.odds_pool import RaceOddsPool
from parimana.base.race_source import RaceSource
from parimana.analyse.regression import RegressionModel
from parimana.analyse.correlation import (
    cor_none,
    cor_by_score,
    cor_by_score_mtx,
    cor_mapping_to_sr,
)
from parimana.analyse.win_rate import extract_win_rate, df_from_win_rate
from parimana.analyse.ability import (
    estimate_ability_map,
    find_uncertainty_map,
)
from parimana.analyse.mvn_model import MvnModel
from parimana.analyse.odds_chance import OddsChance
from parimana.analyse.odds_eval import (
    calc_vote_tally,
)


T = TypeVar("T", bound=Comparable)


@dataclass(frozen=True)
class AnalysisResult(Generic[T]):
    odds_pool: RaceOddsPool
    model: MvnModel[T]
    chances: Mapping[Eye, float]

    @cached_property
    def odds_chance(self) -> OddsChance:
        return OddsChance(self.odds_pool.odds, self.chances)

    @cached_property
    def recommendation(self) -> pd.DataFrame:
        return self.odds_chance.df.query("expected >= 100").sort_values(
            "expected", ascending=False
        )

    def save(self, dir_: Path):
        dir_.mkdir(exist_ok=True, parents=True)
        self.model.save_figures(dir_)
        self.odds_chance.chart.save(dir_ / "oc.png")
        xlname = f"{self.model.name}.xlsx"
        with pd.ExcelWriter(dir_ / xlname) as writer:
            self.recommendation.to_excel(writer, sheet_name="recommend")
            self.odds_chance.df.to_excel(writer, sheet_name="simulation")
            self.model.to_excel(writer)


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


_ppf_smpl = OnePassAnalyser("ppf_smpl", lambda d: cor_by_score(d.ppf, d.members))
_ppf_mtx = OnePassAnalyser(
    "ppf_mtx", lambda d: cor_by_score_mtx(d.ppf_matrix, d.members)
)
_no_cor = OnePassAnalyser("no_cor", lambda d: cor_none(d.members))
_multi = MultiPassAnalyser("multi", [_no_cor, _ppf_mtx])
_twice = MultiPassAnalyser("twice", [_no_cor, _no_cor])

_analysers: Sequence[Analyser[T]] = [_ppf_smpl, _ppf_mtx, _no_cor, _multi, _twice]

analysers: Mapping[str, Analyser[T]] = {a.name: a for a in _analysers}
analyser_names: Sequence[str] = [a.name for a in _analysers]


def default_analyser_names():
    return ["ppf_mtx"]
