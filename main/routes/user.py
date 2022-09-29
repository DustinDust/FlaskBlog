from flask import jsonify

from main import app
from main import db
from main.common.decorators import validate_input, jwt_guard
from main.common.exceptions import (
    UnauthorizedError,
    RecordExistedError,
    RecordNotFoundError,
)
from main.libs.auth import generate_token
from main.models.user import User
from main.schemas.user import UserSchema


@app.post("/user/sign-in")
@validate_input(UserSchema)
def sign_in(username, password, **kwargs):
    user = User.query.filter_by(username=username).one_or_none()
    if user is not None:
        if not user.check_password(password=password):
            raise UnauthorizedError()
        else:
            return jsonify({"access_token": generate_token({"user_id": user.id})})
    else:
        raise RecordNotFoundError()


@app.post("/user/sign-up")
@validate_input(UserSchema)
def sign_up(username, email, password, **kwargs):
    existing_user = User.query.filter_by(username=username).one_or_none()
    if existing_user is not None:
        raise RecordExistedError()

    new_user = User()
    new_user.username = username
    new_user.email = email
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(
        {
            "user_id": new_user.id,
            "access_token": generate_token({"user_id": new_user.id}),
        }
    )


@app.get("/user/me")
@jwt_guard
def get_profile(user_id, **kwargs):
    user = User.query.get(user_id)
    return jsonify(
        {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
        }
    )
