from dataclasses import dataclass
import io
from typing import Generic, Mapping, Optional, TypeVar

import pandas as pd
from matplotlib.figure import Figure

from parimana.base import Eye, Comparable, RaceOddsPool
from parimana.analyse.mvn_model import MvnModel
from parimana.analyse.odds_chance import OddsChance


T = TypeVar("T", bound=Comparable)


@dataclass(frozen=True)
class AnalysisResult(Generic[T]):
    odds_pool: RaceOddsPool
    model: MvnModel[T]
    chances: Mapping[Eye, float]

    @property
    def odds_chance(self) -> OddsChance:
        return OddsChance(self.odds_pool.odds, self.chances)

    def recommend(
        self, query: Optional[str] = None, size: Optional[int] = None
    ) -> pd.DataFrame:
        df = self.odds_chance.df.query("expected >= 100").sort_values(
            "expected", ascending=False
        )
        if query:
            df = df.query(query)
        if size:
            df = df.head(size)

        return df

    def print_recommendation(
        self, query: Optional[str] = None, size: Optional[int] = None
    ) -> pd.DataFrame:
        print()
        print(f"-- Recommendation by {self.model.name} [{query}] --")
        print(self.recommend(query, size))
        print()

    def to_excel(self) -> bytes:
        xlbuf = io.BytesIO()
        with pd.ExcelWriter(xlbuf, engine="openpyxl") as writer:
            self.recommend().to_excel(writer, sheet_name="recommend")
            self.odds_chance.df.to_excel(writer, sheet_name="simulation")
            self.model.au_df().to_excel(writer, sheet_name="au")
            self.model.cor_df().to_excel(writer, sheet_name="cor")
        return xlbuf.getvalue()

    def get_charts(self) -> "AnalysisCharts":
        return AnalysisCharts(
            result=self,
            excel=self.to_excel(),
            odds_chance=fig_to_bytes(self.odds_chance.chart.fig),
            model_box=fig_to_bytes(self.model.plot_box()),
            model_mds=fig_to_bytes(self.model.plot_mds()),
            model_mds_metric=fig_to_bytes(self.model.plot_mds(metric=True)),
        )


def fig_to_bytes(fig: Figure, dpi: int = 300, format: str = "png") -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, dpi=dpi, format=format)
    return buf.getvalue()


@dataclass(frozen=True)
class AnalysisCharts(Generic[T]):
    result: AnalysisResult[T]
    excel: bytes
    odds_chance: bytes
    model_box: bytes
    model_mds: bytes
    model_mds_metric: bytes
