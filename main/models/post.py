from main import db
from .model_mixin import ModelMixin
from .post_tag import post_tag


class Post(ModelMixin, db.Model):
    __tablename__ = "post"

    body = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tags = db.relationship(
        "Tag",
        secondary=post_tag,
        lazy="dynamic",
        backref=db.backref("posts", lazy=True),
    )

    def __repr__(self):
        return "<Post {}>".format(self.body)
