from marshmallow import fields, validates, ValidationError, validate

from .base import BaseSchema


class UserSchema(BaseSchema):
    id = fields.Integer()
    email = fields.Email()
    password = fields.String(required=True, validate=validate.Length(min=6))
    username = fields.String(required=True)

    @validates("password")
    def password_validator(self, value: str):
        has_upper = False
        has_lower = False
        has_number = False
        has_non_ascii = False

        for char in value:
            if char.isupper():
                has_upper = True
            if char.islower():
                has_lower = True
            if not char.isascii():
                has_non_ascii = True
            if char.isnumeric():
                has_number = True

        if has_non_ascii:
            raise ValidationError("Password contains special characters")
        elif not has_lower:
            raise ValidationError("Password must contain lower characters")
        elif not has_upper:
            raise ValidationError("Password must contain upper characters")
        elif not has_number:
            raise ValidationError("Password must contain numeric characters")
