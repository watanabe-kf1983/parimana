from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import pickle
from typing import Any, Callable, Optional


from parimana.io.message import mprint


class Storage(ABC):

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def read_binary(self, key: str) -> Optional[bytes]:
        pass

    @abstractmethod
    def write_binary(self, key: str, binary: bytes) -> None:
        pass

    def read_object(
        self, key: str, *, deserializer: Callable[[bytes], Any] = pickle.loads
    ) -> Optional[Any]:
        if binary := self.read_binary(key):
            return deserializer(binary)
        else:
            return None

    def write_object(
        self,
        key: str,
        obj: object,
        *,
        serializer: Callable[[object], bytes] = pickle.dumps,
    ) -> None:
        return self.write_binary(key, serializer(obj))

    def read_text(self, key: str) -> Optional[str]:
        return self.read_object(key, deserializer=lambda x: x.decode(encoding="utf-8"))

    def write_text(self, key: str, text: str) -> None:
        return self.write_object(
            key, text, serializer=lambda x: x.encode(encoding="utf-8")
        )


@dataclass(frozen=True)
class FileStorage(Storage):
    root_path: Path

    def exists(self, key: str) -> bool:
        file_path = self._get_file_path(key)
        return file_path.exists() and file_path.is_file()

    def read_binary(self, key: str) -> Optional[bytes]:
        file_path = self._get_file_path(key)
        if self.exists(key):
            with open(file_path, "rb") as f:
                mprint(f"reading {file_path} ...")
                return f.read()
        else:
            return None

    def write_binary(self, key: str, binary: bytes) -> None:
        file_path = self._get_file_path(key)
        file_path.parent.mkdir(exist_ok=True, parents=True)
        with open(file_path, "wb") as f:
            mprint(f"writing {file_path} ...")
            f.write(binary)

    def _get_file_path(self, key: str) -> Path:
        return self.root_path / key


@dataclass(frozen=True)
class CachedStorage(Storage):
    original: Storage
    cache: Storage

    def _fetch_to_cache(self, key: str) -> bool:
        if not self.cache.exists(f"fetched:{key}"):
            self.cache.write_binary(f"fetched:{key}", b"T")
            if self.original.exists(key):
                self.cache.write_binary(f"cache:{key}", self.original.read_binary(key))

    def exists(self, key: str) -> bool:
        self._fetch_to_cache(key)
        return self.cache.exists(f"cache:{key}")

    def read_binary(self, key: str) -> Optional[bytes]:
        self._fetch_to_cache(key)
        return self.cache.read_binary(f"cache:{key}")

    def write_binary(self, key: str, binary: bytes) -> None:
        self.cache.write_binary(f"fetched:{key}", b"T")
        self.cache.write_binary(f"cache:{key}", binary)
        self.original.write_binary(key, binary)
