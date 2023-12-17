from dataclasses import dataclass
import io
from typing import Mapping, Optional, Sequence

import pandas as pd
from matplotlib.figure import Figure

from parimana.base import Eye, OddsPool, Contestant
from parimana.analyse.mvn_model import MvnModel
from parimana.analyse.expected import EyeExpectedValue, EyeExpectedValues


@dataclass(frozen=True)
class AnalysisResult:
    odds_pool: OddsPool
    model: MvnModel[Contestant]
    chances: Mapping[Eye, float]

    @property
    def eev(self) -> EyeExpectedValues:
        return EyeExpectedValues.from_odds_and_chances(
            self.odds_pool.odds, self.chances
        )

    def recommend2(
        self, query: Optional[str] = None, size: Optional[int] = None
    ) -> Sequence[EyeExpectedValue]:
        return self.eev.filter(query, size).values()

    def recommend(
        self, query: Optional[str] = None, size: Optional[int] = None
    ) -> pd.DataFrame:
        return self.eev.filter(query, size).df

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
            self.eev.df.to_excel(writer, sheet_name="simulation")
            self.model.au_df().to_excel(writer, sheet_name="au")
            self.model.cor_df().to_excel(writer, sheet_name="cor")
        return xlbuf.getvalue()

    def get_charts(self) -> "AnalysisCharts":
        return AnalysisCharts(
            result=self,
            excel=self.to_excel(),
            odds_chance=fig_to_bytes(self.eev.chart.fig),
            model_box=fig_to_bytes(self.model.plot_box()),
            model_mds=fig_to_bytes(self.model.plot_mds()),
            model_mds_metric=fig_to_bytes(self.model.plot_mds(metric=True)),
        )


def fig_to_bytes(fig: Figure, dpi: int = 300, format: str = "png") -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, dpi=dpi, format=format)
    return buf.getvalue()


@dataclass(frozen=True)
class AnalysisCharts:
    result: AnalysisResult
    excel: bytes
    odds_chance: bytes
    model_box: bytes
    model_mds: bytes
    model_mds_metric: bytes
