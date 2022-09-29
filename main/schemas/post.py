from marshmallow import fields, validate, post_load

from .base import BaseSchema
from .tag import TagSchema


class PostSchema(BaseSchema):
    id = fields.Integer()
    body = fields.String(required=True, validate=validate.Length(max=256))
    user_id = fields.Integer()
    tags = fields.List(fields.Nested(TagSchema()))

    @post_load
    def strip_self(self, data, **kwargs):
        if "body" in data:
            data["body"] = data["body"].strip()
        return data
