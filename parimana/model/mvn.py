from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Sequence, TypeVar
from parimana.model.model import Model
from parimana.situation.situation import Comparable


T = TypeVar("T", bound=Comparable)


@dataclass(frozen=True)
class Ability(Generic[T]):
    contestant: T
    ability: float
    uncertainty: float


@dataclass(frozen=True)
class Correlation(Generic[T]):
    a: T
    b: T
    correlation: float


@dataclass(frozen=True)
class Covariance(Generic[T]):
    a: T
    b: T
    covariance: float


# multivariate_normal
class MvnModel(Model[T]):
    @property
    @abstractmethod
    def correlations(self) -> Sequence[Correlation[T]]:
        pass

    @property
    @abstractmethod
    def abilities(self) -> Sequence[Ability[T]]:
        pass

    @property
    @abstractmethod
    def vc_matrix(self) -> Sequence[Covariance[T]]:
        pass

    @property
    @abstractmethod
    def correlations_map(self) -> Any:
        # 多次元構成法? で描画
        pass
