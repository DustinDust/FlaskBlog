import functools

import jwt
from flask import request
from marshmallow import ValidationError

from main import app
from main.models.post import Post
from main.models.tag import Tag
from .exceptions import RecordNotFoundError, UnauthorizedError, SchemaValidationError


# validate request input with schema
def validate_input(schema, partial: tuple[str] | bool = False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if request.method in ["GET", "DELETE"]:
                data = request.args
            else:
                data = request.get_json()

            try:
                loaded_data = schema().load(data, partial=partial)
            except ValidationError as e:
                raise SchemaValidationError(
                    error_data=e.data, error_message=e.normalized_messages()
                )
            return func(*args, **loaded_data, **kwargs)

        return wrapper

    return decorator


def jwt_guard(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token_string = request.headers["Authorization"].split(" ")[1]
            header_data = jwt.get_unverified_header(token_string)
            decode_data = jwt.decode(
                token_string,
                key=app.config["JWT_SECRET"],
                algorithms=[header_data["alg"]],
            )
            kwargs["user_id"] = decode_data["user_id"]
        except (jwt.InvalidTokenError, KeyError, IndexError):
            raise UnauthorizedError()
        return func(*args, **kwargs)

    return wrapper


def check_post_exist(func):
    @functools.wraps(func)
    def wrapper(*args, post_id, **kwargs):
        post = Post.query.filter_by(id=post_id).one_or_none()
        if post is None:
            raise RecordNotFoundError(error_data={"post_id": post_id})

        kwargs["post"] = post
        return func(*args, **kwargs)

    return wrapper


def check_tag_exist(func):
    @functools.wraps(func)
    def wrapper(*args, tag_id, **kwargs):
        tag = Tag.query.get(tag_id)
        if tag is None:
            raise RecordNotFoundError(error_data={"tag_id": tag_id})
        kwargs["tag"] = tag
        return func(*args, **kwargs)

    return wrapper
