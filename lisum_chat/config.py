from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedmineSettings(BaseModel):
    url: str
    key: str


class BotSettings(BaseModel):
    token: str


class Settings(BaseSettings):
    redmine: RedmineSettings
    bot: BotSettings

    model_config = SettingsConfigDict(env_nested_delimiter="_")


config = Settings()
