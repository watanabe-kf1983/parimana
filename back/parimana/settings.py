from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    file_storage_root_path: str = ".output"
    redis_hostname: str = "localhost"
    redis_port: int = 6379
    redis_id_for_q: int = 0
    redis_id_for_ap: int = 1
    redis_uri_for_q: str = ""
    redis_uri_for_ap: str = ""

    @property
    def redis_q_uri(self):
        return (
            self.redis_uri_for_q
            or f"redis://{self.redis_hostname}:{self.redis_port}/{self.redis_id_for_q}"
        )

    @property
    def redis_ap_uri(self):
        return (
            self.redis_uri_for_ap
            or f"redis://{self.redis_hostname}:{self.redis_port}/{self.redis_id_for_ap}"
        )
