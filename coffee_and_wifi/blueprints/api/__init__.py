from flask import Flask

from .resources import blueprint


def init_app(app: Flask) -> None:
    app.register_blueprint(blueprint)
