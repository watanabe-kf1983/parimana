from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import pickle
from typing import Any, Callable, Optional, Sequence


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

    def batch_exists(self, keys: Sequence[str]) -> Sequence[bool]:
        return [self.exists(key) for key in keys]

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
        file_path.parent.absolute().mkdir(exist_ok=True, parents=True)
        with open(file_path, "wb") as f:
            mprint(f"writing {file_path} ...")
            f.write(binary)

    def _get_file_path(self, key: str) -> Path:
        return self.root_path / key


@dataclass(frozen=True)
class CachedStorage(Storage):
    original: Storage
    cache: Storage

    def _original_to_cache(self, key: str) -> None:
        self.cache.write_binary(f"fetched:{key}", b"T")
        if self.original.exists(key):
            self.cache.write_binary(f"cache:{key}", self.original.read_binary(key))

    def _fetch(self, key: str) -> None:
        if not self.cache.exists(f"fetched:{key}"):
            self._original_to_cache(key)

    def _batch_fetch(self, keys: Sequence[str]) -> None:
        fetched_exists_list = self.cache.batch_exists(
            [f"fetched:{key}" for key in keys]
        )
        for key, fetched_exists in zip(keys, fetched_exists_list):
            if not fetched_exists:
                self._original_to_cache(key)

    def exists(self, key: str) -> bool:
        self._fetch(key)
        return self.cache.exists(f"cache:{key}")

    def batch_exists(self, keys: Sequence[str]) -> Sequence[bool]:
        self._batch_fetch(keys)
        return self.cache.batch_exists([f"cache:{key}" for key in keys])

    def read_binary(self, key: str) -> Optional[bytes]:
        self._fetch(key)
        return self.cache.read_binary(f"cache:{key}")

    def write_binary(self, key: str, binary: bytes) -> None:
        self.cache.write_binary(f"fetched:{key}", b"T")
        self.cache.write_binary(f"cache:{key}", binary)
        self.original.write_binary(key, binary)
