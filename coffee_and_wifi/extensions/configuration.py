from pathlib import Path
from typing import Any

from dynaconf import FlaskDynaconf
from flask import Flask


def init_app(app: Flask, config: dict[str, Any]) -> None:
    FlaskDynaconf(
        app,
        instance_relative_config=True,
        settings_files=['settings.toml'],
        **config
    )
    Path(app.instance_path).mkdir(exist_ok=True)
    app.config.load_extensions()
