from abc import abstractmethod
from dataclasses import dataclass
from typing import Mapping, Tuple, TypeVar
from parimana.model.model import Model
from parimana.situation.situation import Comparable


T = TypeVar("T", bound=Comparable)


@dataclass(frozen=True)
class Ability:
    expected_value: float
    uncertainty: float


# multivariate_normal
class MvnModel(Model[T]):
    @property
    @abstractmethod
    def correlations(self) -> Mapping[Tuple[T, T], float]:
        pass

    @property
    @abstractmethod
    def abilities(self) -> Mapping[T, Ability]:
        pass

    @property
    @abstractmethod
    def covariances(self) -> Mapping[Tuple[T, T], float]:
        pass

    # @property
    # @abstractmethod
    # def correlations_map(self) -> Any:
    #     # 多次元構成法? で描画
    #     pass
