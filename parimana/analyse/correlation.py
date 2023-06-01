from typing import Collection, Iterator, Mapping, Sequence, TypeVar, Tuple
import pandas as pd

from parimana.base.compare import Comparable
from parimana.base.situation import Situation


T = TypeVar("T", bound=Comparable)

# 相関
# https://toukeigaku-jouhou.info/2018/09/13/kind-of-correlation/
# https://cogpsy.jp/win_rate/win_rate-content/uploads/COGPSY-TR-002.pdf


def correlation_none(members: Sequence[T]) -> Mapping[Tuple[T, T], float]:
    return {(a, b): (1 if a == b else 0) for a in members for b in members}


def correlation_by_score(
    scores: Collection[Tuple[Situation[T], Mapping[T, float]]], members: Sequence[T]
) -> Mapping[Tuple[T, T], float]:
    iter = _iter_scores(scores)
    return _correlation_from_score_iter(iter, members)


def correlation_by_score_mtx(
    scores_mtx: Collection[
        Tuple[Situation[T], Mapping[Tuple[T, T], Tuple[float, float]]]
    ],
    members: Sequence[T],
) -> Mapping[Tuple[T, T], float]:
    iter = _iter_scores_mtx(scores_mtx)
    return _correlation_from_score_iter(iter, members)


def _correlation_from_score_iter(
    iter: Iterator[Tuple[Situation, Tuple[T, float], Tuple[T, float]]],
    members: Sequence[T],
) -> Mapping[Tuple[T, T], float]:
    scores_df = _score_iter_to_df(iter)
    cor_sr = _calc_correlation(scores_df)
    return cor_sr_to_mapping(cor_sr, members)


def _calc_correlation(df_scores: pd.DataFrame) -> pd.Series:
    df = df_scores.query("accuracy > 1").copy()
    df["score_a_f"] = df["score_a"] * df["frequency"]
    df["score_b_f"] = df["score_b"] * df["frequency"]
    sum_by_ab = df.groupby(["a", "b"]).sum(numeric_only=True)
    mean_a = (sum_by_ab["score_a_f"] / sum_by_ab["frequency"]).rename("mean_a")
    mean_b = (sum_by_ab["score_b_f"] / sum_by_ab["frequency"]).rename("mean_b")

    df = df.join(mean_a, on=(["a", "b"])).join(mean_b, on=(["a", "b"]))
    df["dev_a"] = df["score_a"] - df["mean_a"]
    df["dev_b"] = df["score_b"] - df["mean_b"]
    df["dev_sq_f_a"] = df["dev_a"] ** 2 * df["frequency"]
    df["dev_sq_f_b"] = df["dev_b"] ** 2 * df["frequency"]
    df["cov_f"] = df["dev_a"] * df["dev_b"] * df["frequency"]

    sum_by_ab = df.groupby(["a", "b"]).sum(numeric_only=True)
    return (
        sum_by_ab["cov_f"]
        / sum_by_ab["dev_sq_f_a"] ** 0.5
        / sum_by_ab["dev_sq_f_b"] ** 0.5
    )


def cor_sr_to_mapping(
    sr: pd.Series, members: Sequence[T]
) -> Mapping[Tuple[T, T], float]:
    members_dict = {str(m): m for m in members}
    return {(members_dict[a], members_dict[b]): cor for (a, b), cor in sr.items()}


def cor_mapping_to_sr(correlations: Mapping[Tuple[T, T], float]) -> pd.Series:
    return pd.DataFrame.from_records(
        [
            {
                "a": str(a),
                "b": str(b),
                "cor": v,
            }
            for (a, b), v in correlations.items()
        ],
        index=["a", "b"],
    )["cor"].rename("cor")


def _score_iter_to_df(
    iterator: Iterator[Tuple[Situation, Tuple[T, float], Tuple[T, float]]]
) -> pd.DataFrame:
    records = [
        {
            "situation": situation.name,
            "frequency": situation.frequency,
            "accuracy": situation.accuracy,
            "a": str(a),
            "b": str(b),
            "score_a": sa,
            "score_b": sb,
        }
        for situation, (a, sa), (b, sb) in iterator
    ]
    return pd.DataFrame.from_records(records)


def _iter_scores(
    scores: Collection[Tuple[Situation[T], Mapping[T, float]]]
) -> Iterator[Tuple[Situation, Tuple[T, float], Tuple[T, float]]]:
    return (
        (situation, (a, sa), (b, sb))
        for situation, mapping in scores
        for a, sa in mapping.items()
        for b, sb in mapping.items()
    )


def _iter_scores_mtx(
    scores: Collection[Tuple[Situation[T], Mapping[Tuple[T, T], Tuple[float, float]]]]
) -> Iterator[Tuple[Situation, Tuple[T, float], Tuple[T, float]]]:
    return (
        (situation, (a, sa), (b, sb))
        for situation, mapping in scores
        for (a, b), (sa, sb) in mapping.items()
    )
