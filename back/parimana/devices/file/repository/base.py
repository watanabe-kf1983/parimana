from dataclasses import dataclass, field
from pathlib import Path
import os


def repository_path() -> Path:
    return Path(os.getenv("FILE_REPO_PATH", ".output"))


@dataclass(frozen=True)
class FileRepositoryBase:
    root_path: Path = field(default_factory=repository_path)
