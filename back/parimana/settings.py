from typing import Literal, Union
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from parimana.io.kvs import FileStorage, Storage


class FileStorageSettings(BaseModel):
    type: Literal["file"] = "file"
    root_dir: str = ".storage"

    def get(self) -> Storage:
        return FileStorage(self.root_dir)


class S3StorageSettings(BaseModel):
    type: Literal["s3"] = "s3"
    prefix_uri: str

    def get(self) -> Storage:
        return FileStorage(self.prefix_uri)


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
