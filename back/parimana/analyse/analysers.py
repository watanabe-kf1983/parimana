from typing import Mapping, Sequence, TypeVar
from parimana.analyse.analyse import Analyser, MultiPassAnalyser, OnePassAnalyser

from parimana.base.situation import Comparable
from parimana.analyse.correlation import (
    cor_none,
    cor_by_score,
    cor_by_score_mtx,
)


T = TypeVar("T", bound=Comparable)


_ppf_smpl = OnePassAnalyser("ppf_smpl", lambda d: cor_by_score(d.ppf, d.members))
_ppf_mtx = OnePassAnalyser(
    "ppf_mtx", lambda d: cor_by_score_mtx(d.ppf_matrix, d.members)
)
_no_cor = OnePassAnalyser("no_cor", lambda d: cor_none(d.members))
_multi = MultiPassAnalyser("multi", [_no_cor, _ppf_mtx])
_twice = MultiPassAnalyser("twice", [_no_cor, _no_cor])

_analysers: Sequence[Analyser[T]] = [_ppf_smpl, _ppf_mtx, _no_cor, _multi, _twice]

analysers: Mapping[str, Analyser[T]] = {a.name: a for a in _analysers}
analyser_names: Sequence[str] = [a.name for a in _analysers]


def default_analyser_names():
    return ["ppf_mtx"]
