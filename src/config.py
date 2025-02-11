from typing import Literal

from pydantic import AnyHttpUrl, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class CORSSettings(BaseModel):
    allow_origins: list[AnyHttpUrl | Literal["*"]] = ["*"]
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]
    allow_credentials: bool = True
    expose_headers: list[str] = []
    max_age: int = 600


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DRONCAST__",
        env_nested_delimiter="__",
        env_file=".env",
        extra="ignore",
    )

    debug: bool = False
    cors: CORSSettings = CORSSettings()
    database: str = "db.sqlite3"


settings = Settings()
