from dataclasses import dataclass
from typing import Iterator, Mapping, Tuple, TypeVar

import numpy as np
import pandas as pd
import plotly.graph_objects as plgo

from parimana.domain.analyse.mvn_model import (
    Ability,
    Model,
    MvnModel,
    calc_chance_of_hit,
)
from parimana.domain.base import Comparable, Eye


T = TypeVar("T", bound=Comparable)


@dataclass
class TripleMvnModel(Model[T]):
    first: MvnModel[T]
    second: MvnModel[T]
    third: MvnModel[T]

    def au_df(self) -> pd.DataFrame:
        return self.first.au_df()

    def cor_df(self) -> pd.DataFrame:
        return self.first.cor_df()

    def plot_box(self) -> plgo.Figure:
        fig = self.first._create_plot_box()
        self.first._add_box(
            fig,
            name="1st place",
            offsetgroup="g1",
            line=dict(color="gold", width=3),
            opacity=0.8,
        )
        self.second._add_box(
            fig,
            name="2nd place",
            offsetgroup="g2",
            line=dict(color="silver", width=3),
            opacity=1.0,
        )
        self.third._add_box(
            fig,
            name="3rd place",
            offsetgroup="g3",
            line=dict(color="#CD7F32", width=2),  # bronze
            opacity=0.5,
        )
        fig.update_layout(boxmode="group")
        return fig

    def plot_mds(self, metric: bool = False) -> plgo.Figure:
        return self.first.plot_mds(metric=metric)

    def simulate_values(self, size: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        return (
            self.first.simulate_values(size),
            self.second.simulate_values(size),
            self.third.simulate_values(size),
        )

    def simulate_values_iter(
        self, n: int, step: int = 1_000_000
    ) -> Iterator[Tuple[np.ndarray, np.ndarray, np.ndarray]]:
        for i in range(0, n, step):
            size = min(step, n - i)
            yield self.simulate_values(size=size)

    def simulate(self, n: int) -> Mapping[Eye, float]:
        columns = ["1st", "2nd", "3rd"]
        trifecta_count = pd.Series(
            [], index=pd.MultiIndex.from_tuples([], names=columns)
        )
        for results in self.simulate_values_iter(n, step=1_000_000):
            trifecta_df = pd.DataFrame(pick_unique_min3(*results), columns=columns)
            trifecta_count = trifecta_count.add(
                trifecta_df.groupby(columns).size(), fill_value=0
            )

        return calc_chance_of_hit(self.first.members, trifecta_count / n)

    @property
    def abilities(self) -> Mapping[T, Ability]:
        return self.first.abilities

    @property
    def covariances(self) -> Mapping[Tuple[T, T], float]:
        return self.first.covariances

    @property
    def correlations(self) -> Mapping[Tuple[T, T], float]:
        return self.first.correlations


def pick_unique_min3(
    first: np.ndarray, second: np.ndarray, third: np.ndarray
) -> np.ndarray[np.int32]:
    """
    first, second, third:  すべて (M, N) の 2-D 配列を想定
    戻り値 :  各行ごとの [j1, j2, j3] を並べた (M, 3) 配列
    """
    # 形状が一致するかだけチェック
    if not (first.shape == second.shape == third.shape):
        raise ValueError("A, B, C の形状が一致しません。")

    M, N = first.shape  # ndim ≠ 2 ならここで unpack エラー
    if N < 3:
        raise ValueError("列数 N は 3 以上必要です。")

    # 1 位
    j1 = np.argsort(first, axis=1)[:, 0]

    # 2 位
    idx_2nd = np.argsort(second, axis=1)
    avail_2nd = idx_2nd != j1[:, None]
    j2 = idx_2nd[np.arange(M), np.argmax(avail_2nd, axis=1)]

    # 3 位
    idx_3rd = np.argsort(third, axis=1)
    avail_3rd = (idx_3rd != j1[:, None]) & (idx_3rd != j2[:, None])
    j3 = idx_3rd[np.arange(M), np.argmax(avail_3rd, axis=1)]

    return np.stack([j1, j2, j3], axis=1).astype(np.int32)
