from flask.testing import FlaskClient
from playhouse.shortcuts import model_to_dict

from coffee_and_wifi.extensions.database import Cafe, db_wrapper


def test_get_random_coffee_should_return_cafe_when_the_database_has_any_records(
    client: FlaskClient,
) -> None:
    response = client.get('/api/v1/cafes/random')
    result = response.json or {}

    assert Cafe.select().count() > 0
    assert response.status_code == 200
    assert 'cafe' in result
    assert type(result['cafe']) == dict


def test_get_random_coffee_should_return_none_when_database_is_empty(
    client: FlaskClient,
) -> None:
    with db_wrapper.database:
        Cafe.delete().execute()

    response = client.get('/api/v1/cafes/random')
    result = response.json or {}

    assert response.status_code == 200
    assert result == {'cafe': None}


def test_get_all_cafes_should_return_all_registered_cafes(
    client: FlaskClient,
) -> None:
    response = client.get('/api/v1/cafes')
    result = response.json or {}

    all_cafes = list(Cafe.select().dicts())

    assert 'cafes' in result
    assert result['cafes'] == all_cafes


def test_create_new_cafe_should_return_http_code_201(
    client: FlaskClient,
) -> None:
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

    stored_cafe = model_to_dict(Cafe.get(Cafe.name == 'Cafe 3'))
    del stored_cafe['id']

    assert response.status_code == 201
    assert cafe_data == stored_cafe


def test_create_new_cafe_should_return_http_code_400_for_missing_data(
    client: FlaskClient,
) -> None:
    cafe_data = {'name': 'Cafe 3'}
    response = client.post('/api/v1/cafes', json=cafe_data)

    assert response.status_code == 400
    assert response.json is not None and 'errors' in response.json
    assert 'NOT NULL constraint failed' in response.json['errors'][0]


def test_create_new_cafe_should_return_http_code_409_when_cafe_already_exists(
    client: FlaskClient,
) -> None:

    with db_wrapper.database:
        stored_cafe = Cafe.get_by_id(2)

    stored_cafe = model_to_dict(stored_cafe)
    del stored_cafe['id']

    response = client.post('/api/v1/cafes', json=stored_cafe)

    assert response.status_code == 409
    assert response.json == {'errors': ['UNIQUE constraint failed: cafe.name']}


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
    response = client.post('/api/v1/cafes', json=cafe_data)

    stored_cafe = Cafe.get(Cafe.name == cafe_data['name'])

    assert response.status_code == 201
    assert cafe_data['id'] != stored_cafe.id


def test_get_cafe_with_id_1_should_return_the_name_of_the_first_cafe(
    client: FlaskClient,
) -> None:
    response = client.get(f'/api/v1/cafes/1')
    result = response.json or {}

    assert response.status_code == 200
    assert result['cafe']['name'] == 'Cafe 1'


def test_get_cafe_should_return_error_404_when_not_found(
    client: FlaskClient,
) -> None:
    response = client.get(f'/api/v1/cafes/3')
    result = response.json or {}

    assert response.status_code == 404
    assert result['errors'][0] == 'Cafe not found.'


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

    stored_cafe = model_to_dict(Cafe.get_by_id(id))

    assert response.status_code == 204
    for key in cafe_data:
        assert cafe_data[key] == stored_cafe[key]


def test_update_non_existent_cafe_should_return_http_code_404(
    client: FlaskClient,
) -> None:
    id = 10
    cafe_data = {
        'name': 'Non-existent Cafe',
    }
    response = client.patch(f'/api/v1/cafes/{id}', json=cafe_data)
    result = response.json or {}

    assert response.status_code == 404
    assert result['errors'][0] == 'Cafe not found.'


def test_update_cafe_should_return_error_400_when_an_empty_json_is_provided(
    client: FlaskClient,
) -> None:
    id = 1
    response = client.patch(f'/api/v1/cafes/{id}', json={})
    result = response.json or {}

    assert response.status_code == 400
    assert 'errors' in result
    assert (
        result['errors'][0] == 'Could not update cafe as no data was provided.'
    )


def test_update_cafe_when_an_id_is_provided_should_not_change_the_id(
    client: FlaskClient,
) -> None:
    id = 1
    response = client.patch(f'/api/v1/cafes/{id}', json={'id': 1000})
    result = response.json or {}

    assert response.status_code == 403
    assert 'errors' in result
    assert result['errors'][0] == 'The cafe id cannot be changed.'


def test_update_cafe_name_to_one_that_already_exists(
    client: FlaskClient,
) -> None:
    id = 1
    response = client.patch(f'/api/v1/cafes/{id}', json={'name': 'Cafe 2'})

    assert response.status_code == 409
    assert response.json == {'errors': ['UNIQUE constraint failed: cafe.name']}


def test_delete_an_existing_cafe_should_return_code_200(
    client: FlaskClient,
) -> None:
    id = 2
    response = client.delete(f'/api/v1/cafes/{id}')

    assert response.status_code == 204
    assert Cafe.get_or_none(id) is None


def test_delete_cafe_with_a_non_existing_id_should_return_error_404(
    client: FlaskClient,
) -> None:
    id = 5
    response = client.delete(f'/api/v1/cafes/{id}')
    result = response.json or {}

    assert response.status_code == 404
    assert result['errors'][0] == 'Cafe not found.'
