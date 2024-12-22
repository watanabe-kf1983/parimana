import os
from pathlib import Path

from parimana.devices.redis.redis_channel import RedisChannelFactory
from parimana.external.boatrace import BoatRace, category_boat
from parimana.external.netkeiba import NetKeibaRace, category_keiba
from parimana.io.kvs import FileStorage


_REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", "localhost")
_REDIS_PORT = os.getenv("REDIS_PORT", "6379")
_REDIS_DB_ID = 0

_redis_uri: str = f"redis://{_REDIS_HOSTNAME}:{_REDIS_PORT}/{_REDIS_DB_ID}"

race_types = [BoatRace, NetKeibaRace]
categories = [category_boat, category_keiba]

_FILE_STORAGE_ROOT_PATH = Path(os.getenv("FILE_REPO_PATH", ".output"))
_storage = FileStorage(_FILE_STORAGE_ROOT_PATH)

analysis_storage = _storage
odds_storage = _storage
schedule_storage = _storage
status_storage = _storage

publish_center = RedisChannelFactory(_redis_uri).publish_center

task_backend_uri = _redis_uri
task_broker_uri = _redis_uri
