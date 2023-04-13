import peewee
from flask import Flask
from playhouse.flask_utils import FlaskDB

db_wrapper = FlaskDB()


class Cafe(db_wrapper.Model):   # type: ignore[name-defined]
    name = peewee.TextField(unique=True)
    location = peewee.TextField()
    opening_time = peewee.TextField()
    closing_time = peewee.TextField()
    coffee_rating = peewee.IntegerField()
    wifi_rating = peewee.IntegerField()
    power_rating = peewee.IntegerField()


def init_app(app: Flask) -> None:
    db_wrapper.init_app(app)

    with db_wrapper.database:
        db_wrapper.database.create_tables([Cafe], safe=True)
