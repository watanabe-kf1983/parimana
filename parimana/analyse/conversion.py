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
