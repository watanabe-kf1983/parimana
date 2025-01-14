from pydantic import BaseModel


class AppInfo(BaseModel):
    status: str
