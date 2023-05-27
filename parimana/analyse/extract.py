from typing import Collection, Mapping, Sequence, TypeVar, Tuple
import numpy as np
import pandas as pd
from parimana.analyse.conversion import (
    correlations_from_sr,
    df_from_scores_mtx,
    win_rate_from_sr,
    df_from_relations,
    df_from_scores,
)

from parimana.base.compare import Comparable
from parimana.base.situation import Situation
from parimana.base.superiority import Relation


T = TypeVar("T", bound=Comparable)


def extract_correlation(
    scores: Collection[Tuple[Situation[T], Mapping[T, int]]], members: Sequence[T]
) -> Mapping[Tuple[T, T], float]:
    df_scores = df_from_scores(scores)
    cor_df = extract_correlation_sr(df_scores)
    return correlations_from_sr(cor_df, members)


def extract_correlation2(
    scores_mtx: Collection[Tuple[Situation[T], Mapping[Tuple[T, T], int]]],
    members: Sequence[T],
) -> Mapping[Tuple[T, T], float]:
    df_scores_mtx = df_from_scores_mtx(scores_mtx)
    cor_df = extract_correlation_sr2(df_scores_mtx)
    return correlations_from_sr(cor_df, members)


def extract_correlation_sr2(df_scores_mtx: pd.DataFrame) -> pd.Series:
    # 相関
    # https://toukeigaku-jouhou.info/2018/09/13/kind-of-correlation/
    # https://cogpsy.jp/win_rate/win_rate-content/uploads/COGPSY-TR-002.pdf
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


def extract_win_rate(
    relations: Collection[Tuple[Situation[T], Collection[Relation[T]]]],
    members: Sequence[T],
) -> Mapping[Tuple[T, T], float]:
    df_rel = df_from_relations(relations)
    wr_sr = extract_win_rate_sr(df_rel)
    return win_rate_from_sr(wr_sr, members)


def extract_win_rate_sr(df_rel: pd.DataFrame) -> pd.Series:
    table = pd.pivot_table(
        df_rel,
        index=["a", "b"],
        columns="superiority_a",
        fill_value=0,
        values="frequency",
        aggfunc=np.sum,
    )
    # table.columns.name = ""
    win_rate = table["SUPERIOR"] / (table["SUPERIOR"] + table["INFERIOR"])
    return win_rate.fillna(0.5).rename("win_rate")
