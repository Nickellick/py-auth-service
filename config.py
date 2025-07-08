from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from pydantic_settings_yaml import YamlBaseSettings

CONFIG_PATH = Path(__file__).parent / "config.yaml"

class Database(BaseModel):
    dbms: str
    sync_driver: str | None
    async_driver: str | None
    host: str
    port: int | None
    user: str
    password: str | None
    database: str
    echo_db: bool

    def build_url(self, is_async: bool = True) -> str:
        sync_driver = f'+{self.sync_driver}' if self.sync_driver else ''
        async_driver = f'+{self.async_driver}' if self.async_driver else ''
        password = f':{self.password}' if self.password else ''
        port = f':{self.port}' if self.port else ''
        return (
            f'{self.dbms}'
            f'{async_driver if is_async else sync_driver}://'
            f'{self.user}'
            f'{password}'
            f'@{self.host}'
            f'{port}'
            f'/{self.database}'
        )

class App(BaseModel):
    host: str
    port: int

class JWT(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

class Config(YamlBaseSettings):
    database: Database
    app: App
    jwt: JWT

    model_config = SettingsConfigDict(yaml_file=f'{Path(__file__).parent / 'config.yaml'}')

config = Config()