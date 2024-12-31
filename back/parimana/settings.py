from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    file_storage_root_path: str = ".output"
    redis_hostname: str = "localhost"
    redis_port: int = 6379
    redis_db_id: int = 0
    redis_db_uri: str = ""

    @property
    def redis_uri(self):
        return (
            self.redis_db_uri
            or f"redis://{self.redis_hostname}:{self.redis_port}/{self.redis_db_id}"
        )
