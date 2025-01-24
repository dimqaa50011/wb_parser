from pathlib import Path
from typing import Literal
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True

env_path = BASE_DIR / ".env" if DEBUG else ".env.local"


DB_DRIVERS = Literal["postgresql+asyncpg"]


class DBConfig(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    name: str

    model_config = SettingsConfigDict(env_prefix="DB_", extra="ignore")

    def uri(self, driver: DB_DRIVERS = "postgresql+asyncpg") -> str:
        return "%(driver)s://%(user)s:%(password)s@%(host)s:%(port)s/%(name)s" % dict(
            driver=driver,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            name=self.name,
        )


class Settings(BaseModel):
    db: DBConfig


settings = Settings(db=DBConfig(_env_file=env_path))


__all__ = ("settings",)
