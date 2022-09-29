from enum import unique
from main import db
from .model_mixin import ModelMixin


class Tag(ModelMixin, db.Model):
    __tablename__ = "tag"

    name = db.Column(db.String(256), nullable=False, unique=True)

    def __repr__(self):
        return "<Tag {}>".format(self.name)
