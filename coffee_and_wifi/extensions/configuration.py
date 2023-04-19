import os
from typing import Literal

from dotenv import load_dotenv
from flask import Flask
from pydantic import BaseModel, BaseSettings

load_dotenv()


class DefaultConfig(BaseSettings):
    SECRET_KEY: str
    TESTING: bool = False
    RESTX_ERROR_404_HELP: bool = False

    class Config:
        env_prefix = 'FLASK_'


class DevConfig(DefaultConfig):
    ENV: Literal['development']
    DATABASE: str = 'sqlite:///instance/cafes.db'


class TestConfig(DefaultConfig):
    ENV: Literal['testing']
    DATABASE: str = 'sqlite:///instance/test.db'
    TESTING: bool = True
    WTF_CSRF_ENABLED: bool = False


class AppConfig(BaseModel):
    config: DevConfig | TestConfig


def get_config() -> DevConfig | TestConfig:
    return AppConfig(
        config={'ENV': os.getenv('ENV', 'development')}  # type: ignore[arg-type]
    ).config


def init_app(app: Flask) -> None:
    config = get_config()
    app.config.from_object(config)
