from http import HTTPStatus
from typing import Any

import pytest
from flask.testing import FlaskClient

from coffee_and_wifi.extensions.database import db_wrapper
from coffee_and_wifi.extensions.database.models import Cafe


def test_get_random_coffee_should_return_cafe_when_the_database_has_any_records(
    client: FlaskClient,
) -> None:
    response = client.get('/api/v1/cafes/random')

    assert Cafe.select().count() > 0
    assert response.status_code == HTTPStatus.OK
    assert type(response.json) == dict
    assert response.json.keys() == Cafe._meta.fields.keys()


def test_get_random_coffee_should_return_error_404_when_database_is_empty(
    client: FlaskClient,
) -> None:
    with db_wrapper.database:
        Cafe.delete().execute()

    response = client.get('/api/v1/cafes/random')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {'message': 'Cafe not found.'}


def test_get_all_cafes_should_return_all_registered_cafes(
    client: FlaskClient,
) -> None:
    response = client.get('/api/v1/cafes/')
    response_content = response.json or {}

    all_cafes = list(Cafe.select().dicts())

    assert response.status_code == HTTPStatus.OK
    assert response_content['count'] == len(all_cafes)
    assert response_content['cafes'] == all_cafes


def test_create_new_cafe_should_return_http_code_201(
    client: FlaskClient,
) -> None:
    cafe_data = {
        'name': 'New Cafe',
        'location': 'https://newcafe.com',
        'opening_time': '07:00',
        'closing_time': '22:00',
        'coffee_rating': 5,
        'wifi_rating': 5,
        'power_rating': 5,
    }
    response = client.post('/api/v1/cafes/', json=cafe_data)
    response_content = response.json or {}

    assert response.status_code == HTTPStatus.CREATED
    assert cafe_data.items() <= response_content.items()


def test_create_new_cafe_should_return_error_400_for_invalid_location(
    client: FlaskClient,
) -> None:
    cafe_data = {
        'name': 'New Cafe',
        'location': 'none',
        'opening_time': '07:00',
        'closing_time': '22:00',
        'coffee_rating': 5,
        'wifi_rating': 5,
        'power_rating': 5,
    }
    response = client.post('/api/v1/cafes/', json=cafe_data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {
        'message': 'CHECK constraint failed: location LIKE "https://%"'
    }


def test_create_new_cafe_should_return_error_400_for_missing_data(
    client: FlaskClient,
) -> None:
    cafe_data = {'name': 'Cafe 3'}
    response = client.post('/api/v1/cafes/', json=cafe_data)
    response_content = response.json or {}

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert 'errors' in response_content
    assert response_content['message'] == 'Input payload validation failed'


def test_create_new_cafe_should_return_error_409_when_cafe_already_exists(
    client: FlaskClient,
) -> None:

    with db_wrapper.database:
        stored_cafe = Cafe.get_by_id(2).as_dict()

    del stored_cafe['id']

    response = client.post('/api/v1/cafes/', json=stored_cafe)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == {
        'message': 'Cafe with the given name already exists.'
    }


def test_create_new_cafe_passing_an_id_should_store_with_a_different_id(
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
    response = client.post('/api/v1/cafes/', json=cafe_data)
    stored_cafe = response.json or {}

    assert response.status_code == HTTPStatus.CREATED
    assert cafe_data['id'] != stored_cafe['id']


def test_get_cafe_with_id_1_should_return_the_name_of_the_first_cafe(
    client: FlaskClient,
) -> None:
    response = client.get(f'/api/v1/cafes/1')
    response_content = response.json or {}

    assert response.status_code == HTTPStatus.OK
    assert response_content['name'] == 'Cafe 1'


def test_get_cafe_should_return_error_404_when_not_found(
    client: FlaskClient,
) -> None:
    response = client.get(f'/api/v1/cafes/4')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {'message': 'Cafe not found.'}


def test_update_cafe_should_return_http_code_204_and_updated_data(
    client: FlaskClient,
) -> None:
    id = 2
    cafe_data = {
        'name': 'Worst Cafe',
        'coffee_rating': 5,
        'wifi_rating': 5,
        'power_rating': 5,
    }
    response = client.patch(f'/api/v1/cafes/{id}', json=cafe_data)
    response_content = response.json or {}

    assert response.status_code == HTTPStatus.OK
    for key in cafe_data:
        assert cafe_data[key] == response_content[key]


def test_update_non_existent_cafe_should_return_error_404(
    client: FlaskClient,
) -> None:
    id = 10
    cafe_data = {
        'name': 'Non-existent Cafe',
    }
    response = client.patch(f'/api/v1/cafes/{id}', json=cafe_data)

    assert response.status_code == 404
    assert response.json == {'message': 'Cafe not found.'}


def test_update_cafe_should_return_error_400_when_an_empty_json_is_provided(
    client: FlaskClient,
) -> None:
    id = 1
    response = client.patch(f'/api/v1/cafes/{id}', json={})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {
        'message': 'Could not update cafe as no data was provided.'
    }


def test_update_cafe_when_an_id_is_provided_should_not_change_the_id(
    client: FlaskClient,
) -> None:
    id = 1
    response = client.patch(f'/api/v1/cafes/{id}', json={'id': 1000})

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {'message': 'The cafe id cannot be changed.'}


@pytest.mark.parametrize(
    'id, cafe_data, expected_error',
    [
        (
            1,
            {
                'coffee_rating': 6,
            },
            'CHECK constraint failed: coffee_rating >= 0 AND coffee_rating <= 5',
        ),
        (
            2,
            {
                'wifi_rating': 6,
            },
            'CHECK constraint failed: wifi_rating >= 0 AND wifi_rating <= 5',
        ),
        (
            3,
            {
                'power_rating': 6,
            },
            'CHECK constraint failed: power_rating >= 0 AND power_rating <= 5',
        ),
        (
            1,
            {
                'coffee_rating': -1,
            },
            'CHECK constraint failed: coffee_rating >= 0 AND coffee_rating <= 5',
        ),
        (
            2,
            {
                'wifi_rating': -1,
            },
            'CHECK constraint failed: wifi_rating >= 0 AND wifi_rating <= 5',
        ),
        (
            3,
            {
                'power_rating': -1,
            },
            'CHECK constraint failed: power_rating >= 0 AND power_rating <= 5',
        ),
    ],
)
def test_update_cafe_should_return_error_400_for_a_rating_field_out_of_range(
    client: FlaskClient,
    id: int,
    cafe_data: dict[str, Any],
    expected_error: str,
) -> None:
    response = client.patch(f'/api/v1/cafes/{id}', json=cafe_data)
    response_content = response.json or {}

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_content['message'] == expected_error


def test_update_cafe_should_return_error_409_when_a_cafe_with_the_given_name_already_exists(
    client: FlaskClient,
) -> None:
    id = 1
    response = client.patch(f'/api/v1/cafes/{id}', json={'name': 'Cafe 2'})

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == {
        'message': 'Cafe with the given name already exists.'
    }


def test_delete_an_existing_cafe_should_return_code_200(
    client: FlaskClient,
) -> None:
    id = 2
    response = client.delete(f'/api/v1/cafes/{id}')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert Cafe.get_or_none(id) is None


def test_delete_cafe_with_a_non_existing_id_should_return_error_404(
    client: FlaskClient,
) -> None:
    id = 5
    response = client.delete(f'/api/v1/cafes/{id}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {'message': 'Cafe not found.'}
