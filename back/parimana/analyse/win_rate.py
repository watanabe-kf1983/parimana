from typing import Collection, Mapping, Sequence, TypeVar, Tuple
import pandas as pd

from parimana.base import Comparable, Situation, Relation


T = TypeVar("T", bound=Comparable)


def extract_win_rate(
    relations: Collection[Tuple[Situation[T], Collection[Relation[T]]]],
    members: Sequence[T],
) -> Mapping[Tuple[T, T], Tuple[float, float]]:
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
        aggfunc="sum",
    )
    win_rate = (
        (table["SUPERIOR"] / (table["SUPERIOR"] + table["INFERIOR"]))
        .fillna(0.5)
        .rename("win_rate")
    )
    win_rate_accuracy = (
        (table["SUPERIOR"] + table["INFERIOR"])
        / (table["SUPERIOR"] + table["INFERIOR"] + table["EQUALS"] + table["UNKNOWN"])
    ).rename("win_rate_acc")

    return win_rate.to_frame().join(win_rate_accuracy)


def win_rate_from_df(
    df: pd.DataFrame, members: Sequence[T]
) -> Mapping[Tuple[T, T], Tuple[float, float]]:
    members_dict = {str(m): m for m in members}
    return {
        (members_dict[a], members_dict[b]): (wr, wr_acc)
        for (a, b), wr, wr_acc in df.itertuples()
    }


def df_from_win_rate(win_rate: Mapping[Tuple[T, T], Tuple[float, float]]) -> pd.Series:
    return pd.DataFrame.from_records(
        [
            {
                "a": str(a),
                "b": str(b),
                "win_rate": r,
                "win_rate_acc": r_acc,
            }
            for (a, b), (r, r_acc) in win_rate.items()
        ],
        index=["a", "b"],
    )


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
