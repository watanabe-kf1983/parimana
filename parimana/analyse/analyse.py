from typing import Mapping, Sequence, Tuple, TypeVar


from parimana.base.situation import Comparable, Distribution
from parimana.analyse.correlation import extract_correlation_none, sr_from_correlations
from parimana.analyse.win_rate import extract_win_rate, sr_from_win_rate
from parimana.analyse.ability import (
    estimate_ability_map,
    find_uncertainty_map,
)
from parimana.analyse.mvn_model import MvnModel


T = TypeVar("T", bound=Comparable)


def analyse(dist: Distribution[T]) -> MvnModel[T]:
    members = dist.members
    # cor = extract_correlation(dist.scores, members)
    # cor2 = extract_correlation2(dist.scores_matrix, members)
    cor_none = extract_correlation_none(members)
    win_rates = extract_win_rate(dist.relations, members)
    return estimate_model(cor_none, win_rates, members)


def estimate_model(
    cor: Mapping[Tuple[T, T], float],
    win_rates: Mapping[Tuple[T, T], float],
    members: Sequence[T],
) -> MvnModel[T]:
    cor_sr = sr_from_correlations(cor)
    wr_sr = sr_from_win_rate(win_rates)
    corwr_df = cor_sr.to_frame().join(wr_sr)
    u_map = find_uncertainty_map(corwr_df)
    a_map = estimate_ability_map(corwr_df, u_map)
    return MvnModel(cor_sr, u_map, a_map, members)
