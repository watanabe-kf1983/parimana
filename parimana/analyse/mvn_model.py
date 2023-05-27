from dataclasses import dataclass
from functools import cached_property
from typing import Generic, Mapping, Sequence, Tuple, TypeVar

import numpy as np
import pandas as pd

from parimana.base.situation import Comparable
from parimana.base.eye import Eye
import parimana.analyse.normal_dist as nd


T = TypeVar("T", bound=Comparable)


@dataclass(frozen=True)
class Ability:
    expected_value: float
    uncertainty: float


@dataclass
class MvnModel(Generic[T]):
    cor_sr: pd.Series
    u_map: pd.Series
    a_map: pd.Series
    members: Sequence[T]

    @cached_property
    def _member_dict(self) -> Mapping[str, T]:
        return {str(m): m for m in self.members}

    def _member_from_name(self, name: str) -> T:
        return self._member_dict[name]

    @cached_property
    def _covariance_sr(self) -> pd.Series:
        cor_sr = self.cor_sr.rename("cor")
        u_map = self.u_map.rename("unc")
        return (
            cor_sr.to_frame()
            .join(u_map, on="a")
            .join(u_map, on="b", rsuffix="_b")
            .apply(
                lambda r: r["unc"] * r["unc_b"] * r["cor"],
                axis=1,
            )
            .rename("cov")
        )

    @cached_property
    def _covariance_mtx(self) -> np.ndarray:
        return pd.pivot_table(
            self._covariance_sr.to_frame(), index="a", columns="b"
        ).values

    def simulate(self, n: int) -> Mapping[Eye, float]:
        mean = self.a_map.values
        cov = self._covariance_mtx

        columns = ["1st", "2nd", "3rd"]
        trifecta_count = pd.Series(
            [], index=pd.MultiIndex.from_tuples([], names=columns)
        )
        for results in nd.simulate(mean, cov, n, step=1_000_000):
            trifecta_df = pd.DataFrame(np.argsort(results)[:, :3], columns=columns)
            trifecta_count = trifecta_count.add(
                trifecta_df.groupby(columns).size(), fill_value=0
            )

        return self._calc_chance_of_hit(trifecta_count / n)

    def _calc_chance_of_hit(self, trif_prob: pd.Series) -> Mapping[Eye, float]:
        trif_prob.index = trif_prob.index.map(
            lambda idxes: tuple(str(self.members[i]) for i in idxes)
        )
        prob_by_eye = [
            (eye.text, p)
            for trifecta, p in trif_prob.items()
            for eye in Eye.eyes_from_names(trifecta)
        ]
        chance_df = pd.DataFrame(prob_by_eye, columns=["eye", "prob"])
        sr = chance_df.groupby(["eye"])["prob"].sum()
        return {Eye(e): v for e, v in sr.items()}

    @cached_property
    def correlations(self) -> Mapping[Tuple[T, T], float]:
        return {
            (self._member_from_name(a), self._member_from_name(b)): cor
            for (a, b), cor in self.cor_sr.items()
        }

    @cached_property
    def abilities(self) -> Mapping[T, Ability]:
        df = self.a_map.rename("ev").to_frame().join(self.u_map.rename("unc"))
        return {
            (self._member_from_name(m)): Ability(ev, unc)
            for m, ev, unc in df.itertuples()
        }

    @cached_property
    def covariances(self) -> Mapping[Tuple[T, T], float]:
        return {
            (self._member_from_name(a), self._member_from_name(b)): cov
            for (a, b), cov in self._covariance_sr.items()
        }

    # @property
    # def correlations_map(self) -> Any:
    #     # 多次元構成法? で描画
    #     return []
