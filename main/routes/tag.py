from flask import request

from main import app, db
from main.common.decorators import check_tag_exist, jwt_guard, validate_input
from main.common.exceptions import RecordExistedError
from main.models.tag import Tag
from main.schemas.tag import TagSchema


@app.get("/tag")
def get_tags():
    form = request.form
    tags = Tag.query.all()
    return TagSchema().jsonify(tags, many=True)


@app.get("/tag/<int:tag_id>")
@check_tag_exist
def get_one_tag(tag, **kwargs):
    return TagSchema.jsonify(tag)


@app.post("/tag")
@jwt_guard
@validate_input(TagSchema)
def create_tag(user_id, name, **kwargs):
    exist_tag = Tag.query.filter_by(name=name).one_or_none()
    if exist_tag is not None:
        raise RecordExistedError(error_data={
            "exist_name": exist_tag.name,
            "new_name": name
        })
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return TagSchema().jsonify(tag)


@app.put("/tag/<int:tag_id>")
@jwt_guard
@validate_input(TagSchema, partial=True)
@check_tag_exist
def update_tag(user_id, name, tag, **kwargs):
    exist_tag = Tag.query.filter_by(name=name).one_or_none()
    if exist_tag is not None:
        raise RecordExistedError(error_data={
            "exist_name": exist_tag.name,
            "new_name": name
        })

    tag.name = name
    db.session.commit()
    return TagSchema().jsonify(tag)


@app.delete("/tag/<int:tag_id>")
@jwt_guard
@check_tag_exist
def delete_tag(user_id, tag, **kwargs):
    db.session.delete(tag)
    db.session.commit()

    return TagSchema().jsonify(tag)
