from pathlib import Path
from typing import Literal
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = False

env_path = BASE_DIR / ".env.local" if DEBUG else BASE_DIR / ".env"


DB_DRIVERS = Literal["postgresql+asyncpg"]


class DBConfig(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    name: str

    model_config = SettingsConfigDict(
        env_file=env_path, env_prefix="DB_", extra="ignore"
    )

    def uri(self, driver: DB_DRIVERS = "postgresql+asyncpg") -> str:
        return "%(driver)s://%(user)s:%(password)s@%(host)s:%(port)s/%(name)s" % dict(
            driver=driver,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            name=self.name,
        )


class SchedulerConfig(BaseSettings):
    interval_minutes: int

    model_config = SettingsConfigDict(
        env_file=env_path, env_prefix="SCHEDULER_", extra="ignore"
    )


class AuthConfig(BaseSettings):
    salt: str

    model_config = SettingsConfigDict(
        env_file=env_path, env_prefix="AUTH_", extra="ignore"
    )


class ProjectSettings(BaseModel):
    debug: bool = DEBUG
    base_dir: Path = BASE_DIR


class BotConfig(BaseSettings):
    token: str

    model_config = SettingsConfigDict(
        env_file=env_path, env_prefix="BOT_", extra="ignore"
    )


class Settings(BaseModel):
    db: DBConfig
    project: ProjectSettings
    scheduler: SchedulerConfig
    auth: AuthConfig
    bot: BotConfig


settings = Settings(
    db=DBConfig.model_validate({}),
    project=ProjectSettings(),
    scheduler=SchedulerConfig.model_validate({}),
    auth=AuthConfig.model_validate({}),
    bot=BotConfig.model_validate({}),
)


__all__ = ("settings",)
