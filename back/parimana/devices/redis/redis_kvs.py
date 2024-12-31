from pathlib import Path
from typing import Optional

import redis

from parimana.io.kvs import Storage


class RedisStorage(Storage):
    def __init__(self, db_uri, prefix: str = "default", ex: int = 86400):
        self.client: redis.Redis = redis.from_url(db_uri)
        self.client.ping()
        self.prefix = f"parimana:kvs:{prefix}"
        self.ex = ex

    def exists(self, key: str) -> bool:
        return bool(self.client.exists(self._get_key(key)))

    def read_binary(self, key: str) -> Optional[bytes]:
        if self.exists(key):
            return bytes(self.client.get(self._get_key(key)))
        else:
            return None

    def write_binary(self, key: str, binary: bytes) -> None:
        self.client.set(self._get_key(key), binary, ex=self.ex)

    def _get_key(self, key: str) -> Path:
        return f"{self.prefix}:{key}"
