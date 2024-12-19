from pathlib import Path
from typing import Optional

from parimana.domain.race import Race
from parimana.app.status import StatusRepository
from parimana.devices.file.repository.base import FileRepositoryBase
import parimana.devices.file.repository.utils as utils


class FileStatusRepository(FileRepositoryBase, StatusRepository):

    def save_process_status(self, race: Race, status: str) -> None:
        utils.write_text(self._race_dir(race) / "status.txt", status)

    def load_process_status(self, race: Race) -> Optional[str]:
        return utils.read_text(self._race_dir(race) / "status.txt")

    def _race_dir(self, race: Race) -> Path:
        dir_ = self.root_path / race.race_id
        dir_.mkdir(exist_ok=True, parents=True)
        return dir_
