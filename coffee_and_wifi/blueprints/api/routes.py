import random

import peewee
from flask import Blueprint, Response, jsonify, request
from flask.typing import ResponseReturnValue

from coffee_and_wifi.extensions.database import Cafe, db_wrapper

api = Blueprint('api', __name__, url_prefix='/api/v1')


@api.get('/cafes/random')
def get_random_cafe() -> ResponseReturnValue:
    cafe = None
    with db_wrapper.database:
        cafes = list(Cafe.select().dicts())

    if cafes:
        cafe = random.choice(cafes)

    return jsonify({'cafe': cafe})


@api.get('/cafes')
def get_all_cafes() -> ResponseReturnValue:
    with db_wrapper.database:
        cafes = list(Cafe.select().dicts())

    return jsonify({'cafes': cafes})


@api.post('/cafes')
def add_cafe() -> ResponseReturnValue:
    payload = request.json or {}
    payload.pop('id', None)

    try:
        with db_wrapper.database.atomic():
            Cafe.create(**payload)
    except peewee.IntegrityError as exception:
        response, status_code = jsonify(errors=[str(exception)]), 400

        if 'UNIQUE' in exception.args[0]:
            status_code = 409

        return response, status_code

    return Response(status=201)
