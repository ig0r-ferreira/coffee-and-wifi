from flask.testing import FlaskClient
from playhouse.shortcuts import model_to_dict

from coffee_and_wifi.extensions.database import Cafe, db_wrapper


def test_get_random_coffee_should_return_cafe_when_the_database_has_any_records(
    client: FlaskClient,
) -> None:
    response = client.get('/api/v1/cafes/random')
    result = response.json or {}

    with db_wrapper.database:
        assert Cafe.select().count() > 0

    assert 'cafe' in result
    assert response.status_code == 200
    assert type(result['cafe']) == dict


def test_get_random_coffee_should_return_null_when_database_is_empty(
    client: FlaskClient,
) -> None:
    with db_wrapper.database:
        Cafe.delete().execute()

    response = client.get('/api/v1/cafes/random')
    result = response.json or {}

    assert response.status_code == 200
    assert result.get('cafe') is None


def test_get_all_cafes(client: FlaskClient) -> None:
    response = client.get('/api/v1/cafes')
    result = response.json or {}

    with db_wrapper.database:
        all_cafes = list(Cafe.select().dicts())

    assert 'cafes' in result
    assert result['cafes'] == all_cafes


def test_create_new_cafe(client: FlaskClient) -> None:
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

    with db_wrapper.database:
        stored_cafe = model_to_dict(Cafe.get(Cafe.name == 'Cafe 3'))
        del stored_cafe['id']

    assert response.status_code == 201
    assert cafe_data == stored_cafe


def test_create_new_cafe_should_return_error_400_for_missing_data(
    client: FlaskClient,
) -> None:
    cafe_data = {'name': 'Cafe 3'}
    response = client.post('/api/v1/cafes', json=cafe_data)

    assert response.status_code == 400
    assert response.json is not None and 'errors' in response.json
    assert 'NOT NULL constraint failed' in response.json['errors'][0]


def test_create_new_cafe_should_return_error_409_when_cafe_already_exists(
    client: FlaskClient,
) -> None:

    with db_wrapper.database:
        cafe = model_to_dict(Cafe.get_by_id(1))
        del cafe['id']

    response = client.post('/api/v1/cafes', json=cafe)

    assert response.status_code == 409
    assert response.json == {'errors': ['UNIQUE constraint failed: cafe.name']}


def test_create_new_cafe_passing_an_id_should_disregard_and_return_a_different_id(
    client: FlaskClient,
) -> None:
    cafe_data = {
        'id': 100000,
        'name': 'Nice Cafe',
        'location': 'https://nicecafe.com',
        'opening_time': '07:00',
        'closing_time': '22:00',
        'coffee_rating': 5,
        'wifi_rating': 5,
        'power_rating': 5,
    }
    response = client.post('/api/v1/cafes', json=cafe_data)

    with db_wrapper.database:
        stored_cafe = Cafe.get(Cafe.name == cafe_data['name'])

    assert response.status_code == 201
    assert cafe_data['id'] != stored_cafe.id
