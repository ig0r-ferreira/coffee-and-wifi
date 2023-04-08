import os
from typing import Any, Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from pydantic import HttpUrl, parse_obj_as

from coffee_and_wifi import create_app
from coffee_and_wifi.extensions.database import get_database
from coffee_and_wifi.models import Cafe


def cafes() -> list[dict[str, Any]]:
    return [
        Cafe(
            cafe_name='Cafe 1',
            cafe_location=parse_obj_as(HttpUrl, 'https://cafe-1.com'),
            opening_time='07:00',
            closing_time='10:00',
            coffee_rating=5,
            wifi_rating=5,
            power_rating=5,
        ).dict(),
        Cafe(
            cafe_name='Cafe 2',
            cafe_location=parse_obj_as(HttpUrl, 'https://cafe-2.com'),
            opening_time='18:00',
            closing_time='22:00',
            coffee_rating=4,
            wifi_rating=3,
            power_rating=2,
        ).dict(),
    ]


@pytest.fixture(scope='session')
def app() -> Generator[Flask, Any, Any]:
    os.environ['ENV'] = 'testing'

    app = create_app()

    with app.app_context():
        get_database().insert_multiple(cafes())

    yield app

    os.environ['ENV'] = 'development'

    with app.app_context():
        get_database().truncate()


@pytest.fixture(scope='session')
def client(app: Flask) -> FlaskClient:
    return app.test_client()
