from typing import Collection, Mapping, Sequence, TypeVar, Tuple
import pandas as pd

from parimana.base.compare import Comparable
from parimana.base.situation import Situation


T = TypeVar("T", bound=Comparable)

# 相関
# https://toukeigaku-jouhou.info/2018/09/13/kind-of-correlation/
# https://cogpsy.jp/win_rate/win_rate-content/uploads/COGPSY-TR-002.pdf


def extract_correlation(
    scores: Collection[Tuple[Situation[T], Mapping[T, int]]], members: Sequence[T]
) -> Mapping[Tuple[T, T], float]:
    df_scores = df_from_scores(scores)
    cor_df = extract_correlation_sr(df_scores)
    return correlations_from_sr(cor_df, members)


def extract_correlation_none(members: Sequence[T]) -> Mapping[Tuple[T, T], float]:
    return {(a, b): (1 if a == b else 0) for a in members for b in members}


def extract_correlation2(
    scores_mtx: Collection[Tuple[Situation[T], Mapping[Tuple[T, T], Tuple[int, int]]]],
    members: Sequence[T],
) -> Mapping[Tuple[T, T], float]:
    df_scores_mtx = df_from_scores_mtx(scores_mtx)
    cor_df = extract_correlation_sr2(df_scores_mtx)
    return correlations_from_sr(cor_df, members)


def extract_correlation_sr2(df_scores_mtx: pd.DataFrame) -> pd.Series:
    df = df_scores_mtx

    df["score_a_f"] = df["score_a"] * df["frequency"]
    df["score_b_f"] = df["score_b"] * df["frequency"]
    sum_by_ab = df.groupby(["a", "b"]).sum(numeric_only=True)
    mean_a = (sum_by_ab["score_a"] / sum_by_ab["frequency"]).rename("mean_a")
    mean_b = (sum_by_ab["score_b"] / sum_by_ab["frequency"]).rename("mean_b")

    df = df.join(mean_a, on=(["a", "b"])).join(mean_b, on=(["a", "b"]))
    df["dev_a"] = df["score_a"] - df["mean_a"]
    df["dev_sq_f_a"] = df["dev_a"] ** 2 * df["frequency"]
    df["dev_b"] = df["score_b"] - df["mean_b"]
    df["dev_sq_f_b"] = df["dev_b"] ** 2 * df["frequency"]

    df["cov_f"] = df["dev_a"] * df["dev_b"] * df["frequency"]

    sum_by_xy = df.groupby(["a", "b"]).sum()
    cor = (
        sum_by_xy["cov_f"]
        / sum_by_xy["dev_sq_f_a"] ** 0.5
        / sum_by_xy["dev_sq_f_b"] ** 0.5
    ).rename_axis(["a", "b"])

    return cor


def extract_correlation_sr(df_scores: pd.DataFrame) -> pd.Series:
    # 相関
    # https://toukeigaku-jouhou.info/2018/09/13/kind-of-correlation/
    # https://cogpsy.jp/win_rate/win_rate-content/uploads/COGPSY-TR-002.pdf
    df = df_scores

    df["score_f"] = df["score"] * df["frequency"]
    sum_by_m = df.groupby(["m"]).sum(numeric_only=True)
    mean_by_m = (sum_by_m["score_f"] / sum_by_m["frequency"]).rename("mean_by_m")

    df = df.join(mean_by_m, on=("m"))
    df["dev"] = df["score"] - df["mean_by_m"]
    df["dev_sq_f"] = df["dev"] ** 2 * df["frequency"]

    mx = pd.merge(df, df, on=["situation", "frequency"])
    mx["cov_f"] = mx["dev_x"] * mx["dev_y"] * mx["frequency"]

    sum_by_xy = mx.groupby(["m_x", "m_y"]).sum()
    cor = (
        sum_by_xy["cov_f"]
        / sum_by_xy["dev_sq_f_x"] ** 0.5
        / sum_by_xy["dev_sq_f_y"] ** 0.5
    ).rename_axis(["a", "b"])

    return cor


def correlations_from_sr(
    sr: pd.Series, members: Sequence[T]
) -> Mapping[Tuple[T, T], float]:
    members_dict = {str(m): m for m in members}
    return {(members_dict[a], members_dict[b]): cor for (a, b), cor in sr.items()}


def sr_from_correlations(correlations: Mapping[Tuple[T, T], float]) -> pd.Series:
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


def df_from_scores(
    scores: Collection[Tuple[Situation[T], Mapping[T, int]]]
) -> pd.DataFrame:
    records = [
        {
            "situation": situation.name,
            "frequency": situation.frequency,
            "m": str(m),
            "score": s,
        }
        for situation, mapping in scores
        for m, s in mapping.items()
    ]
    return pd.DataFrame.from_records(records)


def df_from_scores_mtx(
    scores: Collection[Tuple[Situation[T], Mapping[Tuple[T, T], Tuple[int, int]]]]
) -> pd.DataFrame:
    records = [
        {
            "situation": situation.name,
            "frequency": situation.frequency,
            "a": str(a),
            "b": str(b),
            "score_a": sa,
            "score_b": sb,
        }
        for situation, mapping in scores
        for (a, b), (sa, sb) in mapping.items()
    ]
    return pd.DataFrame.from_records(records)
