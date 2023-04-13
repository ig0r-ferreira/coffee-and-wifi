import os
from typing import Any, Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from coffee_and_wifi import create_app
from coffee_and_wifi.extensions.database import Cafe, db_wrapper


def cafes() -> list[dict[str, str | int]]:
    return [
        {
            'name': 'Cafe 1',
            'location': 'https://cafe-1.com',
            'opening_time': '07:00',
            'closing_time': '10:00',
            'coffee_rating': 5,
            'wifi_rating': 5,
            'power_rating': 5,
        },
        {
            'name': 'Cafe 2',
            'location': 'https://cafe-2.com',
            'opening_time': '18:00',
            'closing_time': '22:00',
            'coffee_rating': 4,
            'wifi_rating': 3,
            'power_rating': 2,
        },
    ]


@pytest.fixture
def app() -> Generator[Flask, Any, Any]:
    os.environ['ENV'] = 'testing'

    app = create_app()

    with db_wrapper.database:
        Cafe.insert_many(cafes()).execute()

    yield app

    with db_wrapper.database:
        Cafe.drop_table(safe=True)

    os.environ['ENV'] = 'development'


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
