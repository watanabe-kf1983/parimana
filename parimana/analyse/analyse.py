from typing import TypeVar

from parimana.analyse.distribution import DistributionForPandas
from parimana.analyse.extract import extract_correlation, extract_win_rate

from parimana.situation.situation import Comparable, Distribution

T = TypeVar("T", bound=Comparable)


def analyse(dist: Distribution[T]) -> None:
    dist_pd = DistributionForPandas(dist)
    cor = extract_correlation(dist_pd.scores)
    win_rates = extract_win_rate(dist_pd.relations)
    print(cor)
    print(win_rates)

    # 多次元構成法? で描画

    # 予想タイムと標準偏差

    # rels から win_rate行列を計算

    # print(win_rate(rels))

    # 全行の標準偏差の対数の分散が収束するまで繰り返す
    # ・win_rate から 与えられたσ(初期値1)を元に距離行列を計算
    # ・距離行列の標準偏差を各行ごとに計算
    # ・全行の標準偏差の対数の分散を計算
    # ・全行の標準偏差の幾何平均に併せてσを補正
    # 標準化した位置の各出場者ごとの平均を算出
    # 標準化した位置の各出場者ごとの平均を算出
