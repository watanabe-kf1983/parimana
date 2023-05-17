from typing import TypeVar

from parimana.situation.situation import Comparable, Distribution
from parimana.analyse.convert import convert_to_dfs

T = TypeVar("T", bound=Comparable)


def analyse(dist: Distribution[T]) -> None:
    score, rels, members = convert_to_dfs(dist)
    print(score)
    print(rels)
