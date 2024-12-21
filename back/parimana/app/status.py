from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, AsyncGenerator

from parimana.infra.message import mprint, mclose, PublishCenter


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
class ProcessStatusManager:
    repo: StatusRepository
    center: PublishCenter

    def start_process(self, process_name: str, check_status: bool = True) -> None:
        status = self.load_status(process_name)
        if status.is_processing and check_status:
            raise Exception(f"{process_name} is processing , can't start")

        self._save_status(process_name, ProcessStatus(is_processing=True))
        mprint("process started.")

    def finish_process(self, process_name: str) -> None:
        self._save_status(process_name, ProcessStatus(is_processing=False))
        mprint("process finished.")
        mprint("====END====")
        mclose()

    def abort_process(self, process_name: str) -> None:
        self._save_status(process_name, ProcessStatus(is_processing=False))
        mprint("process aborted.")
        mprint("====ABEND====")
        mclose()

    def load_status(self, process_name: str) -> ProcessStatus:
        return self.repo.load_process_status(process_name)

    def _save_status(self, process_name: str, status: ProcessStatus) -> None:
        self.repo.save_process_status(process_name, status)

    async def alisten(self, process_name: str) -> AsyncGenerator[str, Any]:
        status = self.load_status(process_name)
        if status.is_processing:
            return self.center.get_channel(process_name).alisten()
        else:
            raise ValueError(f"Not processing, {status=}")
