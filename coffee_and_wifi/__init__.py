from typing import Any

from flask import Flask

from coffee_and_wifi.blueprints import api, user_interface
from coffee_and_wifi.extensions import appearance, configuration, database


def create_app() -> Flask:
    app = Flask(__name__)
    configuration.init_app(app)
    api.init_app(app)
    user_interface.init_app(app)
    appearance.init_app(app)
    database.init_app(app)
    return app
