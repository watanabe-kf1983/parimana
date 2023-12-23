from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel

from parimana.race import Race
from parimana.repository import FileRepository


repo = FileRepository(Path(".output"))


class ProcessStatus(BaseModel):
    is_processing: bool

    def __str__(self):
        if self.is_processing:
            return "PROCESSING"
        else:
            return "DONE"

    @classmethod
    def from_txt(cls, txt: str) -> "ProcessStatus":
        return ProcessStatus(is_processing=("PROCESSING" in txt))


@dataclass
class ProcessStatusManager:
    race: Race

    def start_process(self, check_status: bool = True) -> None:
        status = self.load_status()
        if status.is_processing and check_status:
            raise Exception(f"{self.race.race_id} is processing , can't start")

        self.save_status(ProcessStatus(is_processing=True))

    def finish_process(self) -> None:
        self.save_status(ProcessStatus(is_processing=False))

    def load_status(self) -> ProcessStatus:
        if txt := repo.load_process_status(self.race):
            return ProcessStatus.from_txt(txt)
        else:
            return ProcessStatus(is_processing=False)

    def save_status(self, status: ProcessStatus) -> None:
        repo.save_process_status(self.race, str(status))
