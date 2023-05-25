from dataclasses import dataclass
from typing import Mapping, Sequence, Tuple, TypeVar

import pandas as pd

from parimana.analyse.conversion import sr_from_correlations, sr_from_win_rate
from parimana.analyse.extract import extract_correlation, extract_win_rate
from parimana.analyse.ability import (
    estimate_ability_map,
    find_uncertainty_map,
)
from parimana.situation.situation import Comparable, Distribution


T = TypeVar("T", bound=Comparable)


def analyse(dist: Distribution[T]) -> None:
    members = dist.members
    cor = extract_correlation(dist.scores, members)
    # rels から win_rate行列を計算
    win_rates = extract_win_rate(dist.relations, members)

    return estimate_model(cor, win_rates, members)


def estimate_model(
    cor: Mapping[Tuple[T, T], float],
    win_rates: Mapping[Tuple[T, T], float],
    members: Sequence[T],
):
    cor_sr = sr_from_correlations(cor)
    wr_sr = sr_from_win_rate(win_rates)
    corwr_df = cor_sr.to_frame().join(wr_sr)
    u_map = find_uncertainty_map(corwr_df)
    a_map = estimate_ability_map(corwr_df, u_map)
    return Model(cor_sr, u_map, a_map, members)


@dataclass
class Model:
    cor_df: pd.DataFrame
    u_map: pd.Series
    a_map: pd.Series
    members: Sequence[T]
