from abc import ABC, abstractmethod
from dataclasses import dataclass

from parimana.io.kvs import Storage


@dataclass
class ProcessStatus:
    is_processing: bool

    def __str__(self):
        if self.is_processing:
            return "PROCESSING"
        else:
            return "NOT_PROCESSING"

    @classmethod
    def from_txt(cls, txt: str) -> "ProcessStatus":
        return ProcessStatus(is_processing=(txt == "PROCESSING"))


class StatusRepository(ABC):

    @abstractmethod
    def save_process_status(self, process_name: str, status: ProcessStatus) -> None:
        pass

    @abstractmethod
    def load_process_status(self, process_name: str) -> ProcessStatus:
        pass


@dataclass
class StatusRepositoryImpl(StatusRepository):
    store: Storage

    def save_process_status(self, process_name: str, status: ProcessStatus) -> None:
        self.store.write_text(f"process/{process_name}/status.txt", str(status))

    def load_process_status(self, process_name: str) -> ProcessStatus:
        loaded = self.store.read_text(f"process/{process_name}/status.txt")
        return ProcessStatus.from_txt(loaded)
