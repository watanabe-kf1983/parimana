from typing import Collection, Mapping, Sequence, TypeVar, Tuple
import numpy as np
import pandas as pd

from parimana.base.compare import Comparable
from parimana.base.situation import Situation
from parimana.base.superiority import Relation


T = TypeVar("T", bound=Comparable)


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
    win_rate = table["SUPERIOR"] / (table["SUPERIOR"] + table["INFERIOR"])
    return win_rate.fillna(0.5).rename("win_rate")


def win_rate_from_sr(
    sr: pd.Series, members: Sequence[T]
) -> Mapping[Tuple[T, T], float]:
    members_dict = {str(m): m for m in members}
    return {
        (members_dict[index[0]], members_dict[index[1]]): wr for index, wr in sr.items()
    }


def sr_from_win_rate(win_rate: Mapping[Tuple[T, T], float]) -> pd.Series:
    return pd.DataFrame.from_records(
        [
            {
                "a": str(a),
                "b": str(b),
                "win_rate": v,
            }
            for (a, b), v in win_rate.items()
        ],
        index=["a", "b"],
    )["win_rate"].rename("win_rate")


def df_from_relations(
    relations: Collection[Tuple[Situation[T], Collection[Relation[T]]]]
) -> pd.DataFrame:
    records = [
        {
            "situation": situation.name,
            "frequency": situation.frequency,
            "a": str(rel.a),
            "b": str(rel.b),
            "superiority_a": rel.sa.name,
        }
        for situation, collection in relations
        for rel in collection
    ]
    return pd.DataFrame.from_records(records)
