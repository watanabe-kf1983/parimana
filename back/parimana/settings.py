from pathlib import Path
from typing import Literal, Optional, Union
from urllib.parse import urlparse
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from parimana.devices.s3.s3_kvs import S3Storage
from parimana.io.kvs import FileStorage, Storage


class FileStorageSettings(BaseModel):
    type: Literal["file"] = "file"
    root_dir: str = ".storage"

    def get(self) -> Storage:
        return FileStorage(Path(self.root_dir))


class S3StorageSettings(BaseModel):
    type: Literal["s3"] = "s3"
    uri: Optional[str] = None
    bucket: Optional[str] = None
    prefix: Optional[str] = ""

    @property
    def bucket_and_prefix(self):
        if self.uri:
            parsed = urlparse(self.uri)
            bucket_name = parsed.netloc
            prefix = parsed.path.lstrip("/")
            return bucket_name, prefix
        elif self.bucket:
            return self.bucket, self.prefix
        else:
            raise ValueError("Either URI or BUCKET must be provided.")

    def get(self) -> Storage:
        return S3Storage(*self.bucket_and_prefix)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    storage: Union[FileStorageSettings, S3StorageSettings] = FileStorageSettings()
    redis_endpoint: str = "localhost:6379"
    redis_id_for_q: int = 0
    redis_id_for_ap: int = 1

    @property
    def redis_q_uri(self):
        return f"redis://{self.redis_endpoint}/{self.redis_id_for_q}"

    @property
    def redis_ap_uri(self):
        return f"redis://{self.redis_endpoint}/{self.redis_id_for_ap}"
