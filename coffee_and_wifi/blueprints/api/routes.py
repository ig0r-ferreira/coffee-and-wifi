import random

import peewee
from flask import Blueprint, Response, jsonify, request
from flask.typing import ResponseReturnValue
from playhouse.shortcuts import model_to_dict

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


@api.get('/cafes/<id>')
def get_cafe(id: str) -> ResponseReturnValue:
    with db_wrapper.database:
        cafe = Cafe.get_or_none(int(id))

    if cafe is None:
        return jsonify(errors=['Cafe not found.']), 404

    return jsonify(cafe=model_to_dict(cafe))


@api.patch('/cafes/<id>')
def update_cafe(id: str) -> ResponseReturnValue:
    with db_wrapper.database:
        cafe = Cafe.get_or_none(int(id))

    if cafe is None:
        return jsonify(errors=['Cafe not found.']), 404

    if not request.json:
        return (
            jsonify(errors=['Could not update cafe as no data was provided.']),
            400,
        )

    if 'id' in request.json:
        return (
            jsonify(errors=['The cafe id cannot be changed.']),
            403,
        )

    for key, value in request.json.items():
        setattr(cafe, key, value)

    cafe.save()
    return Response(status=204)
