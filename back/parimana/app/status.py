from typing import Any, AsyncGenerator

from parimana.io.kvs import Storage
from parimana.io.message import mprint, mclose, PublishCenter
from parimana.repository.status import (
    ProcessStatus,
    StatusRepository,
    StatusRepositoryImpl,
)


class ProcessStatusManager:
    def __init__(self, store: Storage, center: PublishCenter):
        self.repo: StatusRepository = StatusRepositoryImpl(store)
        self.center: PublishCenter = center

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
