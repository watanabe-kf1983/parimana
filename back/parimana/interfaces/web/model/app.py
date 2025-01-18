from pydantic import BaseModel


class AppInfo(BaseModel):
    status: str
    auto_analyse: bool
