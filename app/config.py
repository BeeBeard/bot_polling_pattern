# Модель лоя получения настроек из .env

from typing import Optional, Union

from pydantic import Field, SecretStr, EmailStr
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    root: Optional[str] = ""                # Путь к директории webhook бота
    secret: Optional[SecretStr] = ""        # "секрет" для безопасности webhook
    webhook: str = ""


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="db_")

    ip: SecretStr
    port: int
    name: SecretStr
    user: SecretStr
    password: SecretStr

    dialect: str
    async_dialect: str
    driver: Optional[str] = ""

    def pre_conn(self):  # Подготавливаем строку для создания conn
        return (
            f"{self.user.get_secret_value()}:{self.password.get_secret_value()}@"
            f"{self.ip.get_secret_value()}:{self.port}/{self.name.get_secret_value()}{self.driver}"
        )

    @computed_field
    def async_conn(self) -> SecretStr:
        return SecretStr(f"{self.async_dialect}://{self.pre_conn()}")

    @computed_field
    def conn(self) -> SecretStr:
        return SecretStr(f"{self.dialect}://{self.pre_conn()}")


class Config(BaseSettings):
    model_config = SettingsConfigDict()

    project: Project = Field(default_factory=Project)
    author: Author = Field(default_factory=Author)
    bot: BotConfig = Field(default_factory=BotConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()

    def __init__(self, **data):
        super().__init__(**data)
        self.set_bot_path()
        self.set_miniapp_path()  # Включить если miniapp в том же проекте


CONFIG = Config()
