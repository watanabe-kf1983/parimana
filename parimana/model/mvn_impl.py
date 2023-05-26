from dataclasses import dataclass
from typing import Any, Collection, Sequence, TypeVar
import numpy as np

import pandas as pd
from parimana.model.model import Results
from parimana.model.mvn import Ability, Correlation, Covariance, MvnModel
from parimana.situation.situation import Comparable
import parimana.normal_dist.normal_dist as nd
from parimana.vote.eye import eyes


T = TypeVar("T", bound=Comparable)


@dataclass
class MvnModelImpl(MvnModel[T]):
    cor_sr: pd.Series
    u_map: pd.Series
    a_map: pd.Series
    members: Sequence[T]

    def simulate(self, n: float) -> Collection[Results]:
        cor_sr = self.cor_sr.rename("cor")
        u_map = self.u_map.rename("unc")
        print(self.a_map)
        print(u_map)
        print(cor_sr)
        mean = self.a_map.values
        cov_sr = (
            cor_sr.to_frame()
            .join(u_map, on="a")
            .join(u_map, on="b", rsuffix="_b")
            .apply(
                lambda r: r["unc"] * r["unc_b"] * r["cor"],
                axis=1,
            )
            .rename("cov")
        )
        cov = pd.pivot_table(cov_sr.to_frame(), index="a", columns="b").values

        print("simulate start")
        trifecta_columns = ["1st", "2nd", "3rd"]
        trifecta_index = pd.MultiIndex.from_tuples([], names=trifecta_columns)
        trifecta_count = pd.Series([], index=trifecta_index)
        for results in nd.simulate(mean, cov, n):
            trifecta_df = pd.DataFrame(
                np.argsort(results)[:, :3], columns=trifecta_columns
            )
            sr = trifecta_df.groupby(trifecta_columns).size()
            trifecta_count = trifecta_count.add(sr, fill_value=0)
            print(".")

        # print(trifecta_count)
        # res_list = [eyes_from_result(r, self.members) for r in results]

        # 使って標準偏差行列から各馬の走破時計を取得
        # 各馬の走破時計から順位を作成
        # 順位から当たり馬券を判定
        # 理想オッズを計算

        trifecta_count.to_csv("trifecta.csv")
        return trifecta_count

    @property
    def correlations(self) -> Sequence[Correlation[T]]:
        return []

    @property
    def abilities(self) -> Sequence[Ability[T]]:
        return []

    @property
    def vc_matrix(self) -> Sequence[Covariance[T]]:
        return []

    @property
    def correlations_map(self) -> Any:
        # 多次元構成法? で描画
        return []


def eyes_from_result(result: np.ndarray, members: Sequence[T]) -> Sequence[T]:
    mi_list = sorted(zip(members, result), key=lambda t: t[1])
    return eyes([str(m) for m, i in mi_list])
