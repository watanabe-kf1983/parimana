from typing import (
    Collection,
    Dict,
    Mapping,
    Sequence,
    Tuple,
    TypeVar,
)

import pandas as pd

from parimana.situation.compare import Comparable
from parimana.situation.situation import Situation
from parimana.situation.superiority import Relation


T = TypeVar("T", bound=Comparable)


def members_mapping(members: Sequence[T]) -> Mapping[str, T]:
    return {str(m): m for m in members}


def record_from_situation(situation: Situation[T]) -> Dict:
    return {
        "situation": situation.name,
        "frequency": situation.frequency,
    }


def df_from_relations(
    relations: Collection[Tuple[Situation[T], Collection[Relation[T]]]]
) -> pd.DataFrame:
    records = [
        record_from_situation(situation)
        | {
            "a": str(rel.a),
            "b": str(rel.b),
            "superiority_a": rel.sa.name,
        }
        for situation, collection in relations
        for rel in collection
    ]
    return pd.DataFrame.from_records(records)


def df_from_scores(
    scores: Collection[Tuple[Situation[T], Mapping[T, int]]]
) -> pd.DataFrame:
    records = [
        record_from_situation(situation)
        | {
            "m": str(m),
            "score": s,
        }
        for situation, mapping in scores
        for m, s in mapping.items()
    ]
    return pd.DataFrame.from_records(records)


def correlations_from_sr(
    sr: pd.Series, members: Sequence[T]
) -> Mapping[Tuple[T, T], float]:
    members_dict = members_mapping(members)
    return {
        (members_dict[index[0]], members_dict[index[1]]): cor
        for index, cor in sr.items()
    }


def sr_from_correlations(correlations: Mapping[Tuple[T, T], float]) -> pd.Series:
    return pd.DataFrame.from_records(
        [
            {
                "a": str(k[0]),
                "b": str(k[1]),
                "cor": v,
            }
            for k, v in correlations.items()
        ],
        index=["a", "b"],
    )["cor"].rename("cor")


def win_rate_from_sr(
    sr: pd.Series, members: Sequence[T]
) -> Mapping[Tuple[T, T], float]:
    members_dict = members_mapping(members)
    return {
        (members_dict[index[0]], members_dict[index[1]]): wr for index, wr in sr.items()
    }


def sr_from_win_rate(win_rate: Mapping[Tuple[T, T], float]) -> pd.Series:
    return pd.DataFrame.from_records(
        [
            {
                "a": str(k[0]),
                "b": str(k[1]),
                "win_rate": v,
            }
            for k, v in win_rate.items()
        ],
        index=["a", "b"],
    )["win_rate"].rename("win_rate")
