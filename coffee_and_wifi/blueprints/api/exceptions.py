from http import HTTPStatus

import werkzeug.exceptions


class APIException(werkzeug.exceptions.HTTPException):
    def __init__(self, code, message):
        super().__init__()
        self.code = code
        self.description = message


class CafeNotFound(APIException):
    def __init__(self):
        super().__init__(HTTPStatus.NOT_FOUND, 'Cafe not found.')


class CafeAlreadyExists(APIException):
    def __init__(self):
        super().__init__(
            HTTPStatus.CONFLICT, 'Cafe with the given name already exists.'
        )


class NoCafeDataProvided(APIException):
    def __init__(self):
        super().__init__(
            HTTPStatus.BAD_REQUEST,
            'Could not update cafe as no data was provided.',
        )
