from flask import Flask, g
from tinydb import TinyDB


def get_database() -> TinyDB:
    if not hasattr(g, '_database'):
        g._database = TinyDB('data/cafes.json', encoding='utf-8')

    return g._database


def close_database() -> None:
    if hasattr(g, '_database'):
        database: TinyDB = g._database
        database.close()


def init_app(app: Flask) -> None:
    app.teardown_appcontext(lambda exception: close_database())
