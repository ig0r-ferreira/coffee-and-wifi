from http import HTTPStatus

import pytest
from flask.testing import FlaskClient


def test_get_index(client: FlaskClient) -> None:
    response = client.get('/')
    result = response.get_data(as_text=True)

    assert 'Coffee & Wi-fi' in result
    assert 'Want to work in a cafe but need power and wi-fi?' in result


def test_get_all_cafes(client: FlaskClient) -> None:
    response = client.get('/cafes')
    result = response.get_data(as_text=True)

    assert response.status_code == HTTPStatus.OK
    assert 'Cafe 1' in result
    assert 'Cafe 2' in result


def test_get_add_cafe_page(client: FlaskClient) -> None:
    response = client.get('/add')
    assert response.status_code == HTTPStatus.OK


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
    result = response.get_data(as_text=True)

    assert response.status_code == HTTPStatus.OK
    assert 'Cafe created successfully.' in result


@pytest.mark.parametrize('cafe_name', ['CAFE 1', 'cAfE 1', 'cafe 1', 'Cafe 1'])
def test_add_cafe_that_already_exists(
    client: FlaskClient, cafe_name: str
) -> None:

    cafe_data = {
        'cafe_location': 'https://testcafe.com',
        'opening_time': '08:00',
        'closing_time': '22:00',
        'coffee_rating': 4,
        'wifi_rating': 4,
        'power_rating': 4,
    }
    cafe_data['cafe_name'] = cafe_name

    response = client.post('/add', data=cafe_data)
    result = response.get_data(as_text=True)

    assert response.status_code == HTTPStatus.OK
    assert 'Cafe with the given name already exists.' in result
