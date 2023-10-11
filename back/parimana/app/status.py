from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel

from parimana.race import Race
from parimana.repository import FileRepository


repo = FileRepository(Path(".output"))


class Status(BaseModel):
    is_processing: bool
    has_result: bool

    def __str__(self):
        if self.is_processing:
            return "DONE,PROCESSING" if self.has_result else "PROCESSING"
        else:
            return "DONE" if self.has_result else "NOT_START"

    @classmethod
    def from_txt(cls, txt: str) -> "Status":
        return Status(is_processing=("PROCESSING" in txt), has_result=("DONE" in txt))


@dataclass
class StatusManager:
    race: Race

    def start_process(self, check_status: bool = True) -> None:
        status = self.load_status()
        if status.is_processing and check_status:
            raise Exception(f"{self.race.race_id} is processing , can't start")

        self.save_status(Status(is_processing=True, has_result=status.has_result))

    def finish_process(self) -> None:
        self.save_status(Status(is_processing=False, has_result=True))

    def load_status(self) -> Status:
        if txt := repo.load_process_status(self.race):
            return Status.from_txt(txt)
        else:
            return Status(is_processing=False, has_result=False)

    def save_status(self, status: Status) -> None:
        repo.save_process_status(self.race, str(status))
