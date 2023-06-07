from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Callable, Generic, Mapping, Sequence, Tuple, TypeVar

import pandas as pd
from parimana.base.eye import Eye


from parimana.base.situation import Comparable, Distribution
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
from parimana.base.vote import (
    calc_expected_dividend,
    em_to_sr,
    odds_to_df,
)


T = TypeVar("T", bound=Comparable)


@dataclass(frozen=True)
class AnalysisResult(Generic[T]):
    odds: Mapping[Eye, float]
    model: MvnModel[T]
    chances: Mapping[Eye, float]
    expected: Mapping[Eye, float]

    @cached_property
    def simulation(self) -> pd.DataFrame:
        return (
            odds_to_df(self.odds)
            .join(em_to_sr(self.chances, "chance"), how="left")
            .join(em_to_sr(self.expected, "expected"), how="left")
            .fillna(0)
            .sort_values(["type", "eye"])
        )

    def print_recommend(self) -> None:
        print()
        print(f"-- Recommendation by {self.model.name} --")
        print(self.recommendation)
        print()

    @cached_property
    def recommendation(self) -> pd.DataFrame:
        return self.simulation.sort_values("expected", ascending=False).head(10)

    def save(self, dir_: Path):
        dir_.mkdir(exist_ok=True, parents=True)
        self.model.save_figures(dir_)
        xlname = f"{self.model.name}.xlsx"
        with pd.ExcelWriter(dir_ / xlname) as writer:
            self.recommendation.to_excel(writer, sheet_name="recommend")
            self.simulation.to_excel(writer, sheet_name="simulation")
            self.model.to_excel(writer)


@dataclass(frozen=True)
class Analyser(Generic[T]):
    name: str
    cor_extractor: Callable[[Distribution[T]], Mapping[Tuple[T, T], float]]

    def analyse(
        self, odds: Mapping[Eye, float], dist: Distribution[T], simulation_count: int
    ) -> AnalysisResult[T]:
        print(f"estimating model by '{self.name}' ...")
        model = self.estimate_model(dist)
        print(f"simulating '{model.name}' ...")
        chances = model.simulate(simulation_count)
        expected = calc_expected_dividend(odds, chances)
        return AnalysisResult(odds, model, chances, expected)

    def estimate_model(self, dist: Distribution[T]) -> MvnModel[T]:
        win_rates = extract_win_rate(dist.relations, dist.members)
        wr_df = df_from_win_rate(win_rates)
        cor = self.cor_extractor(dist)
        cor_sr = cor_mapping_to_sr(cor)
        corwr_df = cor_sr.to_frame().join(wr_df)
        u_map = find_uncertainty_map(corwr_df)
        a_map = estimate_ability_map(corwr_df, u_map)

        return MvnModel(cor_sr, u_map, a_map, dist.members, self.name)


_analysers: Sequence[Analyser[T]] = [
    Analyser("ppf_smpl", lambda d: cor_by_score(d.ppf, d.members)),
    Analyser("ppf_mtx", lambda d: cor_by_score_mtx(d.ppf_matrix, d.members)),
    Analyser("no_cor", lambda d: cor_none(d.members)),
]

analysers: Mapping[str, Analyser[T]] = {a.name: a for a in _analysers}
analyser_names: Sequence[str] = [a.name for a in _analysers]


def default_analyser_names():
    return ["ppf_mtx"]
