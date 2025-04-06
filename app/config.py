# Модель лоя получения настроек из .env

from typing import Optional, Union, Any

from pydantic import Field, SecretStr, EmailStr
from pydantic import computed_field, field_validator
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


class MiniAppConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="miniapp_")

    ip: Optional[str] = ""              # ip на хост где расположен (front) miniapp бота
    host: Optional[str] = ""            # Ссылка на хост где расположен (front) miniapp бота
    port: Optional[int] = None          # Порт для miniapp бота
    root: Optional[str] = ""            # Путь к директории miniapp бота
    secret: Optional[SecretStr] = ""    # "секрет" для безопасности miniapp
    path: str = ""

    # @computed_field
    # def path(self) -> str:
    #     return self.host + self.root

class ApiConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="api_")

    ip: Optional[str] = ""              # ip на API
    host: Optional[str] = ""            # ip на API
    port: Optional[int] = None          # Порт для API
    root: Optional[str] = ""            # Путь к директории API
    secret: Optional[SecretStr] = ""    # "секрет" для безопасности API
    version: Optional[str] = ""         # Версия API
    # path: str = ""

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


class AllowedConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="allowed_")

    ips: Any

    # noinspection PyMethodParameters
    @field_validator("ips")
    def parse_items(cls, v):

        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return []


class Config(BaseSettings):
    model_config = SettingsConfigDict()

    project: Project = Field(default_factory=Project)
    author: Author = Field(default_factory=Author)
    bot: BotConfig = Field(default_factory=BotConfig)
    miniapp: MiniAppConfig = Field(default_factory=MiniAppConfig)
    api: ApiConfig = Field(default_factory=ApiConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    allowed: AllowedConfig = Field(default_factory=AllowedConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()

    def set_bot_path(self):
        self.bot.webhook = self.bot.host + self.project.root + self.bot.root

    def set_api_path(self):
        port = f":{self.api.port}" if self.api.port else ""
        self.api.path = self.api.ip + port + self.project.root + self.api.root + self.api.version

    def set_miniapp_path(self):
        self.miniapp.path = self.miniapp.host + self.project.root + self.miniapp.root

    def __init__(self, **data):
        super().__init__(**data)
        self.set_bot_path()
        self.set_miniapp_path()  # Включить если miniapp в том же проекте


CONFIG = Config()

# pprint.pprint(CONFIG.model_dump())
