from http import HTTPStatus

from flask.testing import FlaskClient

from coffee_and_wifi.extensions.database import db_wrapper
from coffee_and_wifi.extensions.database.models import Cafe


def test_get_index(client: FlaskClient) -> None:
    response = client.get('/')
    response_content = response.get_data(as_text=True)

    assert 'Coffee & Wifi' in response_content
    assert (
        'Want to work in a cafe but need power and wifi?' in response_content
    )


def test_get_all_cafes(client: FlaskClient) -> None:
    response = client.get('/cafes')
    response_content = response.get_data(as_text=True)

    assert 'All Cafes' in response_content
    assert 'Return to home page' in response_content


def test_get_add_cafe_form(client: FlaskClient) -> None:
    response = client.get('/add')
    response_content = response.get_data(as_text=True)

    assert 'Add a new cafe' in response_content
    assert 'Submit' in response_content
    assert 'See all cafes' in response_content


def test_add_cafe(client: FlaskClient) -> None:
    cafe_data = {
        'cafe_name': 'The best cafe',
        'cafe_location': 'https://thebestcafe.com',
        'opening_time': '07:00',
        'closing_time': '10:00',
        'coffee_rating': 5,
        'wifi_rating': 5,
        'power_rating': 5,
    }
    response = client.post('/add', data=cafe_data)
    assert response.status_code == HTTPStatus.FOUND


def test_add_cafe_that_already_exists(
    client: FlaskClient,
) -> None:

    with db_wrapper.database:
        cafe_data = Cafe.get_by_id(2).as_dict()

    del cafe_data['id']
    cafe_data['cafe_name'] = cafe_data.pop('name')
    cafe_data['cafe_location'] = cafe_data.pop('location')

    response = client.post('/add', data=cafe_data)

    assert response.status_code == HTTPStatus.OK
    assert (
        'Error: Cafe with the given name already exists.'
        in response.get_data(as_text=True)
    )
