from typing import Any

import peewee
from playhouse.shortcuts import model_to_dict

from . import db_wrapper


class Cafe(db_wrapper.Model):
    name = peewee.TextField()
    location = peewee.TextField()
    opening_time = peewee.TextField()
    closing_time = peewee.TextField()
    coffee_rating = peewee.IntegerField()
    wifi_rating = peewee.IntegerField()
    power_rating = peewee.IntegerField()

    class Meta:
        constraints = [
            peewee.SQL('UNIQUE ("name" COLLATE NOCASE)'),
            peewee.Check('location LIKE "https://%"'),
            peewee.Check('coffee_rating >= 0 AND coffee_rating <= 5'),
            peewee.Check('wifi_rating >= 0 AND wifi_rating <= 5'),
            peewee.Check('power_rating >= 0 AND power_rating <= 5'),
        ]

    def as_dict(self) -> dict[str, Any]:
        return model_to_dict(self)
