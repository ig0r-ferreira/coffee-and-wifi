from flask import Flask
from flask.testing import FlaskClient
from tinydb import Query

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


def test_create_new_cafe(app: Flask, client: FlaskClient) -> None:
    cafe_data = {
        'name': 'Cafe 3',
        'location': 'https://cafe-3.com',
        'opening_time': '07:00',
        'closing_time': '22:00',
        'coffee_rating': 5,
        'wifi_rating': 5,
        'power_rating': 5,
    }
    response = client.post('/api/v1/cafes', json=cafe_data)

    assert response.status_code == 201
    with app.app_context():
        database = get_database()
        assert cafe_data in database.search(Query().name == 'Cafe 3')


def test_create_new_cafe_should_return_error_400_for_missing_data(
    client: FlaskClient,
) -> None:
    cafe_data = {'name': 'Cafe 3'}
    response = client.post('/api/v1/cafes', json=cafe_data)

    assert response.status_code == 400
    assert response.json is not None
    assert 'errors' in response.json


def test_create_new_cafe_should_return_error_409_when_cafe_already_exists(
    app: Flask, client: FlaskClient
) -> None:
    with app.app_context():
        cafe = get_database().get(doc_id=1)

    response = client.post('/api/v1/cafes', json=cafe)

    assert response.status_code == 409
    assert response.json == {
        'errors': [f'There is already a cafe named {cafe["name"]!a}.']
    }
