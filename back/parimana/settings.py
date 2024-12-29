import os
from pathlib import Path


FILE_STORAGE_ROOT_PATH = Path(os.getenv("FILE_REPO_PATH", ".output"))

REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB_ID = 0

REDIS_DB_URI = f"redis://{REDIS_HOSTNAME}:{REDIS_PORT}/{REDIS_DB_ID}"
