from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedmineSettings(BaseModel):
    url: str
    key: str


class BotSettings(BaseModel):
    token: str


class Database(BaseModel):
    path: str


class Settings(BaseSettings):
    redmine: RedmineSettings
    bot: BotSettings
    database: Database
    repliesnumber: int

    model_config = SettingsConfigDict(
        env_nested_delimiter="_", env_file=".env", env_file_encoding="utf-8"
    )


config = Settings()
