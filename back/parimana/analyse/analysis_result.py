from dataclasses import dataclass
import io
from typing import Mapping, Optional, Sequence

import pandas as pd

from parimana.base import Eye, OddsPool, Contestant
from parimana.message import mprint
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
        self, query: Optional[str] = None
    ) -> Sequence[EyeExpectedValue]:
        return self.eev.filter(query).values()

    def recommend(
        self, query: Optional[str] = None, size: Optional[int] = None
    ) -> pd.DataFrame:
        return self.eev.filter(query, size).df

    def print_recommendation(
        self, query: Optional[str] = None, size: Optional[int] = None
    ) -> pd.DataFrame:
        mprint()
        mprint(f"-- Recommendation by {self.model.name} [{query}] --")
        mprint(self.recommend(query, size))
        mprint()

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
            odds_chance=self.eev.chart().fig.to_json(),
            model_box=self.model.plot_box().to_json(),
            # model_mds=self.model.plot_mds().to_json(),
            # model_mds_metric=self.model.plot_mds(metric=True).to_json(),
        )


@dataclass(frozen=True)
class AnalysisCharts:
    result: AnalysisResult
    excel: bytes
    odds_chance: str
    model_box: str
    # model_mds: str
    # model_mds_metric: str
