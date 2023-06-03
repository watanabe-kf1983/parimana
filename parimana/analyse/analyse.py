from dataclasses import dataclass
from typing import Callable, Generic, Mapping, Sequence, Tuple, TypeVar


from parimana.base.situation import Comparable, Distribution
from parimana.analyse.correlation import (
    cor_none,
    cor_by_score,
    cor_by_score_mtx,
    cor_mapping_to_sr,
)
from parimana.analyse.win_rate import extract_win_rate, df_from_win_rate
from parimana.analyse.ability import (
    estimate_ability_map,
    find_uncertainty_map,
)
from parimana.analyse.mvn_model import MvnModel


T = TypeVar("T", bound=Comparable)


@dataclass(frozen=True)
class Analyser(Generic[T]):
    name: str
    cor_extractor: Callable[[Distribution[T]], Mapping[Tuple[T, T], float]]

    def estimate_model(self, dist: Distribution[T]) -> MvnModel[T]:
        print(f"estimate model by '{self.name}' ...")

        print(" extracting win_rates...")
        win_rates = extract_win_rate(dist.relations, dist.members)
        wr_df = df_from_win_rate(win_rates)

        print(" estimating correlations...")
        cor = self.cor_extractor(dist)
        cor_sr = cor_mapping_to_sr(cor)

        print(" estimating uncertainly...")
        corwr_df = cor_sr.to_frame().join(wr_df)
        u_map = find_uncertainty_map(corwr_df)

        print(" estimating ability...")
        a_map = estimate_ability_map(corwr_df, u_map)

        print(" done.")
        return MvnModel(cor_sr, u_map, a_map, dist.members, self.name)


_analysers: Sequence[Analyser[T]] = [
    # Analyser("score_sgl", lambda d: cor_by_score(d.scores, d.members)),
    # Analyser("score_mtx", lambda d: cor_by_score_mtx(d.scores_matrix, d.members)),
    # Analyser("ppf", lambda d: cor_by_score(d.ppf, d.members)),
    Analyser("ppf_mtx", lambda d: cor_by_score_mtx(d.ppf_matrix, d.members)),
    # Analyser("none_cor", lambda d: cor_none(d.members)),
]


def analyse(dist: Distribution[T]) -> Sequence[MvnModel[T]]:
    return [a.estimate_model(dist) for a in _analysers]
