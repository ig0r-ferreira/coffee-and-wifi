from flask import Flask

from .routes import ui


def init_app(app: Flask) -> None:
    app.register_blueprint(ui)
