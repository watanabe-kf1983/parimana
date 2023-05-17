from functools import cached_property
from typing import (
    Collection,
    Generic,
    Mapping,
    Sequence,
    Tuple,
    TypeVar,
)
from dataclasses import dataclass

import pandas as pd

from parimana.situation.compare import Comparable
from parimana.situation.situation import Situation, Distribution


T = TypeVar("T", bound=Comparable)


@dataclass(frozen=True)
class SituationForPandas(Generic[T]):
    situation: Situation[T]
    members: Sequence[Tuple[T, str]]

    @cached_property
    def record(self) -> Mapping:
        return {
            "situation": self.situation.name,
            "frequency": self.situation.frequency,
        }

    @cached_property
    def relations(self) -> pd.DataFrame:
        records = [
            self.record
            | {
                "a": a_str,
                "b": b_str,
                "superiority_a": self.situation.get_superiority(a, b).name,
            }
            for a, a_str in self.members
            for b, b_str in self.members
        ]
        return pd.DataFrame.from_records(records)

    @cached_property
    def scores(self) -> pd.DataFrame:
        records = [
            self.record
            | {
                "m": m_str,
                "score": self.situation.get_score(m),
            }
            for (m, m_str) in self.members
        ]
        return pd.DataFrame.from_records(records)


@dataclass(frozen=True)
class DistributionForPandas(Generic[T]):
    distribution: Distribution[T]
    members: Sequence[Tuple[T, str]]

    @cached_property
    def _situ_4pds(self) -> Collection[SituationForPandas[T]]:
        return [
            SituationForPandas(s, self.members) for s in self.distribution.situations
        ]

    @cached_property
    def relations(self) -> pd.DataFrame:
        return pd.concat((s.relations for s in self._situ_4pds), ignore_index=True)

    @cached_property
    def scores(self) -> pd.DataFrame:
        return pd.concat((s.scores for s in self._situ_4pds), ignore_index=True)


def dataframes(distribution: Distribution[T]):
    members = [(m, str(m)) for m in distribution.situations[0].members]
    member_dict = {k: v for v, k in members}
    dfp = DistributionForPandas(distribution, members)
    return (dfp.scores, dfp.relations, member_dict)
