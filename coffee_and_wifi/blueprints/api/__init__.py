from flask import Flask

from .routes import api


def init_app(app: Flask) -> None:
    app.register_blueprint(api)
