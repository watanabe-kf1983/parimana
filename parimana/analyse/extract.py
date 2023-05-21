import numpy as np
import pandas as pd


def extract_correlation(scores: pd.DataFrame) -> pd.DataFrame:
    # 相関
    # https://toukeigaku-jouhou.info/2018/09/13/kind-of-correlation/
    # https://cogpsy.jp/win_rate/win_rate-content/uploads/COGPSY-TR-002.pdf

    scores["score_f"] = scores["score"] * scores["frequency"]
    gp = scores.groupby(["m"]).sum(numeric_only=True)
    gp["ave"] = gp["score_f"] / gp["frequency"]

    scores = scores.join(gp[["ave"]], on=("m"))
    scores["delta"] = scores["score"] - scores["ave"]
    scores["delta_sq_f"] = scores["delta"] ** 2 * scores["frequency"]

    scores = pd.merge(scores, scores, on=["situation", "frequency"])
    scores["multi_f"] = scores["delta_x"] * scores["delta_y"] * scores["frequency"]

    gp = scores.groupby(["m_x", "m_y"])[
        ["frequency", "delta_sq_f_x", "delta_sq_f_y", "multi_f"]
    ].sum(numeric_only=True)
    gp["correlation"] = (
        gp["multi_f"] / gp["delta_sq_f_x"] ** 0.5 / gp["delta_sq_f_y"] ** 0.5
    )
    gp = gp[["correlation"]]

    table2 = pd.pivot_table(
        gp.reset_index(), index="m_x", columns="m_y", values="correlation"
    )
    print(table2)
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
    table2 = pd.pivot_table(
        table.reset_index(),
        index="a",
        columns="b",
        values="win_rate",
        margins=True,
    )
    print(table2)

    return table
