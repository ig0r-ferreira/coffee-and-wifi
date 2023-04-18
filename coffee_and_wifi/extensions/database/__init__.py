from flask import Flask
from playhouse.flask_utils import FlaskDB

db_wrapper = FlaskDB()


def init_app(app: Flask) -> None:
    db_wrapper.init_app(app)
    models = db_wrapper.Model.__subclasses__()

    with db_wrapper.database:
        db_wrapper.database.create_tables(models, safe=True)
