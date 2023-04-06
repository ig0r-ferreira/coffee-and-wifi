from flask import Flask
from flask_bootstrap import Bootstrap5

bootstrap = Bootstrap5()


def init_app(app: Flask) -> None:
    bootstrap.init_app(app)
