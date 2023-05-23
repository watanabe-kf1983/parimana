from typing import Mapping, Sequence, Tuple, TypeVar
from parimana.analyse.conversion import df_from_correlations, df_from_win_rate

from parimana.analyse.extract import extract_correlation, extract_win_rate
from parimana.situation.situation import Comparable, Distribution

T = TypeVar("T", bound=Comparable)


def estimate_sd(
    cor: Mapping[Tuple[T, T], float],
    win_rates: Mapping[Tuple[T, T], float],
    members: Sequence[T],
) -> Mapping[T, float]:
    cor_df = df_from_correlations(cor)
    wr_df = df_from_win_rate(win_rates)

    df = cor_df.join(wr_df)
    df["sa"] = 1
    df["sb"] = 1

    print(df)

    # rels から win_rate行列を計算
    # 全行の標準偏差の対数の分散が収束するまで繰り返す
    # ・win_rate から 与えられたσ(初期値1)を元に距離行列を計算
    # ・距離行列の標準偏差を各行ごとに計算
    # ・全行の標準偏差の対数の分散を計算
    # ・全行の標準偏差の幾何平均に併せてσを補正
    # 標準化した位置の各出場者ごとの平均を算出

    return {}


def analyse(dist: Distribution[T]) -> None:
    members = dist.members
    cor = extract_correlation(dist.scores, members)
    win_rates = extract_win_rate(dist.relations, members)
    # 標準偏差
    sd = estimate_sd(cor, win_rates, members)
    print(sd)
    # 多次元構成法? で描画
