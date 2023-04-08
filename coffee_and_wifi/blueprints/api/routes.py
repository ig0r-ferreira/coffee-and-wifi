import random

from flask import Blueprint, jsonify
from flask.typing import ResponseReturnValue

from coffee_and_wifi.extensions.database import get_database

api = Blueprint('api', __name__, url_prefix='/api/v1')


@api.get('/cafes/random')
def get_random_cafe() -> ResponseReturnValue:
    cafe = None
    cafes = get_database().all()
    if cafes:
        cafe = random.choice(cafes)
    return jsonify({'cafe': cafe})


@api.get('/cafes')
def get_all_cafes() -> ResponseReturnValue:
    return jsonify({'cafes': get_database().all()})
