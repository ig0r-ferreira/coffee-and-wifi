import random
import re

import pydantic
from flask import Blueprint, Response, jsonify, request
from flask.typing import ResponseReturnValue

from coffee_and_wifi.extensions.database import Query, get_database
from coffee_and_wifi.models import Cafe

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


@api.post('/cafes')
def add_cafe() -> ResponseReturnValue:
    payload = request.json or {}

    try:
        cafe = Cafe(**payload)
    except pydantic.ValidationError as exception:
        return jsonify(errors=exception.errors()), 400

    database = get_database()
    if database.search(Query().name.matches(cafe.name, flags=re.IGNORECASE)):
        return (
            jsonify(errors=[f'There is already a cafe named {cafe.name!a}.']),
            409,
        )

    database.insert(cafe.dict())
    return Response(status=201)
