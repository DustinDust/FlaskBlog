import http

from flask import jsonify, make_response
from marshmallow import ValidationError

from main import app
from .exceptions import BaseError


def register_error_handler():
    @app.errorhandler(BaseError)
    def handle_base_exception(e):
        return e.to_response()

    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        return make_response(
            jsonify(
                {
                    "error_message": e.normalized_messages(),
                    "error_data": e.data,
                }
            ),
            http.HTTPStatus.BAD_REQUEST,
        )

    @app.errorhandler(500)
    def handle_internal_server_error(e):
        return make_response(
            jsonify(
                {
                    "error_message": str(e.original_exception),
                }
            ),
            500,
        )
