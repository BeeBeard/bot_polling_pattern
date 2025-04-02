# Модель лоя получения настроек из .env
from pydantic import BaseModel, model_validator, validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, EmailStr
from typing import Optional, Union
import pprint
import os
class ConfigBase(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

class Project(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="project_")

    name: Optional[str] = ""
    version: Optional[str] = ""
    info: Optional[str] = ""
    root: str


class Author(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="author_")

    tg_id: Optional[int] = None
    tg_username: Optional[str] = ""
    email: Optional[Union[EmailStr, str]] = ""


class BotConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="tg_")

    token: SecretStr
    is_webhook: bool = False

    ip: Optional[str] = ""                  # ip на хост где висит webhook бота
    host: Optional[str] = ""                # Ссылка на хост где висит webhook бота
    port: Optional[int] = ""                # Порт для бота
    webhook: Optional[str] = ""             # Путь к директории webhook бота
    secret: Optional[SecretStr] = ""        # "секрет" для безопасности webhook

    @computed_field
    def path(self) -> str:
        return self.host + self.webhook


class MiniAppConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="miniapp_")

    ip: Optional[str] = ""              # ip на хост где расположен (front) miniapp бота
    host: Optional[str] = ""            # Ссылка на хост где расположен (front) miniapp бота
    port: Optional[int] = None          # Порт для miniapp бота
    root: Optional[str] = ""            # Путь к директории miniapp бота
    secret: Optional[SecretStr] = ""    # "секрет" для безопасности miniapp

    @computed_field
    def path(self) -> str:
        return self.host + self.root

class ApiConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="api_")

    ip: Optional[str] = ""              # ip на API
    host: Optional[str] = ""            # ip на API
    port: Optional[int] = None          # Порт для API
    root: Optional[str] = ""            # Путь к директории API
    secret: Optional[SecretStr] = ""    # "секрет" для безопасности API
    version: Optional[str] = ""         # Версия API

    @computed_field
    def path(self) -> str:
        port = f":{self.port}" if self.port else ""
        return f"{self.ip}{port}{self.root}{self.version}"

    @computed_field
    def root_path(self) -> str:
        return f"{self.root}{self.version}"

class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="db_")

    ip: SecretStr
    port: int
    name: str
    user: str
    password: SecretStr

    dialect: str
    async_dialect: str
    driver: Optional[str] = ""


class Config(BaseSettings):
    project: Project = Field(default_factory=Project)
    author: Author = Field(default_factory=Author)
    bot: BotConfig = Field(default_factory=BotConfig)
    miniapp: MiniAppConfig = Field(default_factory=MiniAppConfig)
    api: ApiConfig = Field(default_factory=ApiConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()


# if __name__ == "__main__":
#     # main()

CONFIG = Config()
# pprint.pprint(CONFIG.model_dump())
