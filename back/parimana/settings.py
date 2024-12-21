import os

import parimana.devices.file.repository as file_repo
from parimana.devices.redis.redis_channel import RedisChannelFactory
from parimana.external.boatrace import BoatRace, category_boat
from parimana.external.netkeiba import NetKeibaRace, category_keiba


_REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", "localhost")
_REDIS_PORT = os.getenv("REDIS_PORT", "6379")
_REDIS_DB_ID = 0

_redis_uri: str = f"redis://{_REDIS_HOSTNAME}:{_REDIS_PORT}/{_REDIS_DB_ID}"

race_types = [BoatRace, NetKeibaRace]
categories = [category_boat, category_keiba]

analysis_repository = file_repo.FileAnalysisRepository()
schedule_repository = file_repo.FileScheduleRepository()
status_repository = file_repo.FileStatusRepository()

publish_center = RedisChannelFactory(_redis_uri).publish_center

task_backend_uri = _redis_uri
task_broker_uri = _redis_uri
