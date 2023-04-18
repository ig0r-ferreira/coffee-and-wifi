from typing import Any

import peewee
from playhouse.shortcuts import model_to_dict

from . import db_wrapper


class Cafe(db_wrapper.Model):
    name = peewee.TextField(unique=True)
    location = peewee.TextField()
    opening_time = peewee.TextField()
    closing_time = peewee.TextField()
    coffee_rating = peewee.IntegerField()
    wifi_rating = peewee.IntegerField()
    power_rating = peewee.IntegerField()

    def as_dict(self) -> dict[str, Any]:
        return model_to_dict(self)
