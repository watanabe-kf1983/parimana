from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from typing import Generic, Iterator, Mapping, Sequence, Tuple, TypeVar

import numpy as np
import pandas as pd
import plotly.graph_objects as plgo
from sklearn.manifold import MDS

from parimana.domain.base import Comparable, Eye
import parimana.domain.analyse.normal_dist as nd


T = TypeVar("T", bound=Comparable)


@dataclass(frozen=True)
class Ability:
    expected_value: float
    uncertainty: float


@dataclass
class Model(ABC, Generic[T]):
    name: str

    @abstractmethod
    def au_df(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def cor_df(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def plot_box(self) -> plgo.Figure:
        pass

    @abstractmethod
    def plot_mds(self) -> plgo.Figure:
        pass

    @abstractmethod
    def simulate(self, n: int) -> Mapping[Eye, float]:
        pass

    @property
    @abstractmethod
    def abilities(self) -> Mapping[T, Ability]:
        pass

    @property
    @abstractmethod
    def covariances(self) -> Mapping[Tuple[T, T], float]:
        pass

    @property
    @abstractmethod
    def correlations(self) -> Mapping[Tuple[T, T], float]:
        pass


@dataclass
class MvnModel(Model[T]):
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

    def au_df(self) -> pd.DataFrame:
        return self.a_map.rename("abi").to_frame().join(self.u_map.rename("unc"))

    def cor_df(self) -> pd.DataFrame:
        return pd.pivot_table(self.cor_sr.to_frame(), index="a", columns="b")

    def plot_box(self) -> plgo.Figure:
        fig = self._create_plot_box()
        self._add_box(fig)
        return fig

    def _create_plot_box(self) -> plgo.Figure:
        fig = plgo.Figure(
            layout=dict(
                title=dict(text="Predicted finishing time for all contestants"),
                xaxis_title="Finishing time"
                + " (0: mean time of all contestants,"
                + "<br> 1: geometric mean of SD for each contestant)",
                yaxis_title="Contestant",
                margin=dict(t=50, b=50, r=20, l=50, autoexpand=True),
            )
        )
        return fig

    def _add_box(self, fig: plgo.Figure, **kwargs) -> None:
        names = self.a_map.index
        mean = self.a_map
        sd = self.u_map
        iqr = sd * 1.34898
        fig.add_trace(
            plgo.Box(
                y=names,
                orientation="h",
                median=mean,
                q1=mean - iqr * 0.5,
                q3=mean + iqr * 0.5,
                lowerfence=mean - iqr * 2.0,
                upperfence=mean + iqr * 2.0,
                mean=mean,
                sd=sd,
                **kwargs,
            )
        )
        fig.update_layout(
            hovermode="y",
        )

    def plot_mds(self, metric: bool = False) -> plgo.Figure:
        dist = self.cor_sr * (-1) + 1
        distance_df = pd.pivot_table(dist.to_frame(), index="a", columns="b")
        mds = MDS(
            n_components=2,
            metric=metric,
            dissimilarity="precomputed",
            random_state=0,
            normalized_stress="auto",
        )
        pos = mds.fit_transform(distance_df.values)

        scatter = plgo.Scatter(
            x=pos[:, 0],
            y=pos[:, 1],
            mode="markers+text",
            text=[str(m) for m in self.members],
            textposition="top center",
        )
        layout = plgo.Layout(yaxis=dict(scaleanchor="x"))
        return plgo.Figure(data=[scatter], layout=layout)

    def simulate_values(self, size: int) -> np.ndarray:
        mean = self.a_map.values
        cov = self._covariance_mtx
        return nd.rvs(mean=mean, cov=cov, size=size)

    def simulate_values_iter(
        self, n: int, step: int = 1_000_000
    ) -> Iterator[np.ndarray]:
        for i in range(0, n, step):
            size = min(step, n - i)
            yield self.simulate_values(size=size)

    def simulate(self, n: int) -> Mapping[Eye, float]:
        columns = ["1st", "2nd", "3rd"]
        trifecta_count = pd.Series(
            [], index=pd.MultiIndex.from_tuples([], names=columns)
        )
        for results in self.simulate_values_iter(n, step=1_000_000):
            trifecta_df = pd.DataFrame(np.argsort(results)[:, :3], columns=columns)
            trifecta_count = trifecta_count.add(
                trifecta_df.groupby(columns).size(), fill_value=0
            )

        return calc_chance_of_hit(self.members, trifecta_count / n)

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


def calc_chance_of_hit(
    members: Sequence[T], trif_prob: pd.Series
) -> Mapping[Eye, float]:
    trif_prob.index = trif_prob.index.map(
        lambda idxes: tuple(str(members[i]) for i in idxes)
    )
    prob_by_eye = [
        (eye.text, p)
        for trifecta, p in trif_prob.items()
        for eye in Eye.eyes_from_places(trifecta)
    ]
    chance_df = pd.DataFrame(prob_by_eye, columns=["eye", "prob"])
    sr = chance_df.groupby(["eye"])["prob"].sum()
    return {Eye(e): v for e, v in sr.items()}
