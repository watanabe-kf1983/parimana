import numpy as np
import pandas as pd


def extract_correlation(scores: pd.DataFrame) -> pd.DataFrame:
    # 相関
    # https://toukeigaku-jouhou.info/2018/09/13/kind-of-correlation/
    # https://cogpsy.jp/win_rate/win_rate-content/uploads/COGPSY-TR-002.pdf

    scores["score_f"] = scores["score"] * scores["frequency"]
    gp = scores.groupby(["m"]).sum(numeric_only=True)
    gp["mean"] = gp["score_f"] / gp["frequency"]

    scores = scores.join(gp[["mean"]], on=("m"))
    scores["deviation"] = scores["score"] - scores["mean"]
    scores["deviation_sq_f"] = scores["deviation"] ** 2 * scores["frequency"]

    scores = pd.merge(scores, scores, on=["situation", "frequency"])
    scores["cov_f"] = (
        scores["deviation_x"] * scores["deviation_y"] * scores["frequency"]
    )

    gp = scores.groupby(["m_x", "m_y"])[
        ["frequency", "deviation_sq_f_x", "deviation_sq_f_y", "cov_f"]
    ].sum(numeric_only=True)
    gp["cor"] = (
        gp["cov_f"] / gp["deviation_sq_f_x"] ** 0.5 / gp["deviation_sq_f_y"] ** 0.5
    )
    gp = gp[["cor"]]

    return gp


def extract_win_rate(relations: pd.DataFrame) -> pd.DataFrame:
    table = pd.pivot_table(
        relations,
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
