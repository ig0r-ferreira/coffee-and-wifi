import random
from http import HTTPStatus

from flask import Blueprint
from flask_restx import Api, Resource, fields

from coffee_and_wifi.extensions.database import IntegrityError, db_wrapper
from coffee_and_wifi.extensions.database.models import Cafe

from .exceptions import (
    APIException,
    CafeAlreadyExists,
    CafeNotFound,
    NoCafeDataProvided,
)

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(
    blueprint,
    version='1.0',
    title='Cafe and Wi-fi API',
    description='A simple Cafe and Wi-fi API',
)

namespace = api.namespace('cafes', description='Cafe Operations')

cafe_model = api.model(
    'Cafe',
    {
        'id': fields.Integer(readonly=True),
        'name': fields.String(required=True),
        'location': fields.String(required=True),
        'opening_time': fields.String(required=True),
        'closing_time': fields.String(required=True),
        'coffee_rating': fields.Integer(required=True, min=0, max=5),
        'wifi_rating': fields.Integer(required=True, min=0, max=5),
        'power_rating': fields.Integer(required=True, min=0, max=5),
    },
)

cafe_list_model = api.model(
    'CafeList',
    {
        'count': fields.Integer(required=True),
        'cafes': fields.List(fields.Nested(cafe_model)),
    },
)


@namespace.route('/')
class List(Resource):
    @namespace.response(HTTPStatus.OK, 'Success', cafe_list_model)
    @namespace.marshal_with(cafe_list_model)
    def get(self):
        """List all cafes"""
        cafes = list(Cafe.select().dicts())
        return {'count': len(cafes), 'cafes': cafes}

    @namespace.expect(cafe_model, validate=True)
    @namespace.response(
        HTTPStatus.CREATED, 'Cafe created successfully', cafe_model
    )
    @namespace.response(
        HTTPStatus.CONFLICT, 'Cafe with the given name already exists'
    )
    @namespace.response(
        HTTPStatus.BAD_REQUEST, 'Input payload validation failed'
    )
    def post(self):
        """Create a new cafe"""
        payload = api.payload
        payload.pop('id', None)

        try:
            with db_wrapper.database.atomic():
                new_cafe = Cafe.create(**payload)
        except IntegrityError as exception:
            error_msg = str(exception)

            if error_msg == 'UNIQUE constraint failed: cafe.name':
                raise CafeAlreadyExists()

            raise APIException(HTTPStatus.BAD_REQUEST, error_msg)

        return Item(self.api).get(new_cafe.id), HTTPStatus.CREATED


@namespace.route('/random')
class Random(Resource):
    @namespace.response(HTTPStatus.OK, 'Success', cafe_model)
    @namespace.response(HTTPStatus.NOT_FOUND, 'Cafe not found')
    @namespace.marshal_with(cafe_model)
    def get(self):
        """Get a random cafe"""
        cafes = List(self.api).get().get('cafes', [])

        if not cafes:
            raise CafeNotFound()

        return random.choice(cafes)


@namespace.route('/<int:id>')
@namespace.response(HTTPStatus.NOT_FOUND, 'Cafe not found')
class Item(Resource):
    @namespace.response(HTTPStatus.OK, 'Success', cafe_model)
    @namespace.marshal_with(cafe_model)
    def get(self, id: int):
        """Get a specific cafe"""
        cafe: Cafe = Cafe.get_or_none(id)

        if cafe is None:
            raise CafeNotFound()

        return cafe.as_dict()

    @namespace.response(HTTPStatus.OK, 'Success', cafe_model)
    @namespace.response(
        HTTPStatus.CONFLICT, 'Cafe with the given name already exists'
    )
    @namespace.response(
        HTTPStatus.BAD_REQUEST, 'Input payload validation failed'
    )
    @namespace.expect(cafe_model, validate=False)
    def patch(self, id: int):
        """Update a specific cafe"""
        payload = api.payload

        if not payload:
            raise NoCafeDataProvided()

        if 'id' in payload:
            raise APIException(
                HTTPStatus.FORBIDDEN, 'The cafe id cannot be changed.'
            )

        cafe = Cafe.get_or_none(id)

        if cafe is None:
            raise CafeNotFound()

        for key, value in payload.items():
            setattr(cafe, key, value)

        try:
            cafe.save()
        except IntegrityError as exception:
            error_msg = str(exception)

            if error_msg == 'UNIQUE constraint failed: cafe.name':
                raise CafeAlreadyExists()

            raise APIException(HTTPStatus.BAD_REQUEST, error_msg)

        return Item(self.api).get(id), HTTPStatus.OK

    @namespace.response(HTTPStatus.NO_CONTENT, 'Success')
    def delete(self, id: int):
        """Delete a specific cafe"""
        cafe = Cafe.get_or_none(id)

        if cafe is None:
            raise CafeNotFound()

        cafe.delete_instance()
        return '', HTTPStatus.NO_CONTENT
