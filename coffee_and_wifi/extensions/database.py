from flask import Flask, current_app, g
from tinydb import TinyDB


def get_database() -> TinyDB:
    if not hasattr(g, '_database'):
        g._database = TinyDB(current_app.config['DATABASE_PATH'])

    return g._database


def close_database() -> None:
    if hasattr(g, '_database'):
        database: TinyDB = g._database
        database.close()


def init_app(app: Flask) -> None:
    app.teardown_appcontext(lambda exception: close_database())
