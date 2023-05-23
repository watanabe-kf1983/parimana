from typing import Collection, Mapping, Sequence, TypeVar, Tuple
import numpy as np
import pandas as pd
from parimana.analyse.conversion import (
    correlations_from_df,
    win_rate_from_df,
    df_from_relations,
    df_from_scores,
)

from parimana.situation.compare import Comparable
from parimana.situation.situation import Situation
from parimana.situation.superiority import Relation


T = TypeVar("T", bound=Comparable)


def extract_correlation(
    scores: Collection[Tuple[Situation[T], Mapping[T, int]]], members: Sequence[T]
) -> Mapping[Tuple[T, T], float]:
    df_scores = df_from_scores(scores)
    cor_df = extract_correlation_df(df_scores)
    return correlations_from_df(cor_df, members)


def extract_correlation_df(df_scores: pd.DataFrame) -> pd.DataFrame:
    # 相関
    # https://toukeigaku-jouhou.info/2018/09/13/kind-of-correlation/
    # https://cogpsy.jp/win_rate/win_rate-content/uploads/COGPSY-TR-002.pdf
    df = df_scores

    df["score_f"] = df["score"] * df["frequency"]
    mean_df = df.groupby(["m"]).sum(numeric_only=True)
    mean_df["mean"] = mean_df["score_f"] / mean_df["frequency"]
    mean_df = mean_df[["mean"]]

    df = df.join(mean_df, on=("m"))
    df["dev"] = df["score"] - df["mean"]
    df["dev_sq_f"] = df["dev"] ** 2 * df["frequency"]

    df = pd.merge(df, df, on=["situation", "frequency"])
    df["cov_f"] = df["dev_x"] * df["dev_y"] * df["frequency"]

    cor = df.groupby(["m_x", "m_y"])
    cor = cor[["dev_sq_f_x", "dev_sq_f_y", "cov_f"]].sum()
    cor["cor"] = cor["cov_f"] / cor["dev_sq_f_x"] ** 0.5 / cor["dev_sq_f_y"] ** 0.5
    cor = cor[["cor"]]
    cor.index.names = ["a", "b"]

    return cor


def extract_win_rate(
    relations: Collection[Tuple[Situation[T], Collection[Relation[T]]]],
    members: Sequence[T],
) -> Mapping[Tuple[T, T], float]:
    df_rel = df_from_relations(relations)
    wr_df = extract_win_rate_df(df_rel)
    return win_rate_from_df(wr_df, members)


def extract_win_rate_df(df_rel: pd.DataFrame) -> pd.DataFrame:
    table = pd.pivot_table(
        df_rel,
        index=["a", "b"],
        columns="superiority_a",
        fill_value=0,
        values="frequency",
        aggfunc=np.sum,
    )
    table.columns.name = ""
    table["win_rate"] = table["SUPERIOR"] / (table["SUPERIOR"] + table["INFERIOR"])
    table = table[["win_rate"]].fillna(0.5)
    return table
