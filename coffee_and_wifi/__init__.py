from flask import Flask

from coffee_and_wifi.extensions import configuration


def create_app(**config) -> Flask:
    app = Flask(__name__)
    configuration.init_app(app, config)

    return app
