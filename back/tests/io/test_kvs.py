from typing import Optional
from parimana.io.kvs import CachedStorage, Storage


class DictStorage(Storage):

    def __init__(self, name=""):
        self.dict = {}
        self.name = name

    def exists(self, key: str) -> bool:
        return key in self.dict

    def read_binary(self, key: str) -> Optional[bytes]:
        return self.dict.get(key)

    def write_binary(self, key: str, binary: bytes) -> None:
        print(f"DictStorage {self.name}: SET {key} <- {binary}")
        self.dict[key] = binary


def test_cached_kvs_batch_exists():

    original = DictStorage("org")
    original.write_text("a", "hello")

    target = CachedStorage(original=original, cache=DictStorage("cac"))
    assert target.batch_exists(["a", "b", "c"]) == [True, False, False]

    target.write_text("b", "hello")

    assert target.batch_exists(["a", "b", "c"]) == [True, True, False]
    assert target.original.batch_exists(["a", "b", "c"]) == [True, True, False]
