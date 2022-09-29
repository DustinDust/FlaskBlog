from marshmallow import fields, validate, post_load

from .base import BaseSchema


class TagSchema(BaseSchema):
    id = fields.Integer()
    name = fields.String(validate=validate.Length(max=256))

    @post_load
    def strip_self(self, data, **kwargs):
        if "name" in data:
            data["name"] = data["name"].strip()
        return data
