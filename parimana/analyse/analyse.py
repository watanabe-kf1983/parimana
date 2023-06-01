from typing import Mapping, Sequence, Tuple, TypeVar


from parimana.base.situation import Comparable, Distribution
from parimana.analyse.correlation import (
    correlation_none,
    correlation_by_score,
    correlation_by_score_mtx,
    cor_mapping_to_sr,
)
from parimana.analyse.win_rate import extract_win_rate, sr_from_win_rate
from parimana.analyse.ability import (
    estimate_ability_map,
    find_uncertainty_map,
)
from parimana.analyse.mvn_model import MvnModel


T = TypeVar("T", bound=Comparable)


def analyse(dist: Distribution[T]) -> Mapping[str, MvnModel[T]]:
    members = dist.members
    win_rates = extract_win_rate(dist.relations, members)
    print(" estimating correlations...")
    cors = {
        "by_score": correlation_by_score(dist.scores, members),
        "by_score_mtx": correlation_by_score_mtx(dist.scores_matrix, members),
        "by_ppf": correlation_by_score(dist.ppf, members),
        "by_ppf_mtx": correlation_by_score_mtx(dist.ppf_matrix, members),
        "none": correlation_none(members),
    }
    return {
        name: estimate_model(cor, win_rates, members, name)
        for name, cor in cors.items()
    }


def estimate_model(
    cor: Mapping[Tuple[T, T], float],
    win_rates: Mapping[Tuple[T, T], float],
    members: Sequence[T],
    name: str,
) -> MvnModel[T]:
    print(f" estimating {name}...")
    cor_sr = cor_mapping_to_sr(cor)
    wr_sr = sr_from_win_rate(win_rates)
    corwr_df = cor_sr.to_frame().join(wr_sr)
    u_map = find_uncertainty_map(corwr_df)
    a_map = estimate_ability_map(corwr_df, u_map)
    return MvnModel(cor_sr, u_map, a_map, members, name)
