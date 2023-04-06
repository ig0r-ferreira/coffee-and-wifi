from flask import Flask

from coffee_and_wifi.blueprints import user_interface
from coffee_and_wifi.extensions import appearance


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_prefixed_env()

    user_interface.init_app(app)
    appearance.init_app(app)
    return app
