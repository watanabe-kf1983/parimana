from pathlib import Path

from parimana.app.status import ProcessStatus, StatusRepository
from parimana.devices.file.repository.base import FileRepositoryBase
import parimana.devices.file.repository.utils as utils


class FileStatusRepository(FileRepositoryBase, StatusRepository):

    def save_process_status(self, process_name: str, status: ProcessStatus) -> None:
        utils.write_text(self._process_dir(process_name) / "status.txt", str(status))

    def load_process_status(self, process_name: str) -> ProcessStatus:
        return ProcessStatus.from_txt(
            utils.read_text(self._process_dir(process_name) / "status.txt")
        )

    def _process_dir(self, process_name: str) -> Path:
        dir_ = self.root_path / "process" / process_name
        dir_.mkdir(exist_ok=True, parents=True)
        return dir_
