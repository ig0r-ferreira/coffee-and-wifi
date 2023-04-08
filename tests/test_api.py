from flask import Flask
from flask.testing import FlaskClient

from coffee_and_wifi.extensions.database import get_database
from coffee_and_wifi.models import Cafe


def test_get_random_coffee_should_return_cafe_when_the_database_has_any_records(
    app: Flask,
    client: FlaskClient,
) -> None:
    response = client.get('/api/v1/cafes/random')
    result = response.json or {}
    cafe = result.get('cafe')

    with app.app_context():
        assert len(get_database().all()) > 0

    assert response.status_code == 200
    assert type(cafe) == dict
    assert cafe.keys() == Cafe.__fields__.keys()


def test_get_random_coffee_should_return_null_when_database_is_empty(
    app: Flask,
    client: FlaskClient,
) -> None:
    with app.app_context():
        get_database().truncate()

    response = client.get('/api/v1/cafes/random')
    result = response.json or {}

    assert response.status_code == 200
    assert result.get('cafe') is None


def test_get_all_cafes(app: Flask, client: FlaskClient) -> None:
    response = client.get('/api/v1/cafes')
    result = response.json or {}

    with app.app_context():
        all_cafes = get_database().all()

    assert 'cafes' in result
    assert result['cafes'] == all_cafes
