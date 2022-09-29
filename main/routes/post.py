from flask import jsonify

from main import app, db
from main.common.decorators import check_post_exist, jwt_guard, validate_input
from main.common.exceptions import RecordNotFoundError, ForbiddenAccessError
from main.models.post import Post
from main.models.tag import Tag
from main.schemas.base import PageSchema
from main.schemas.post import PostSchema


@app.get("/post")
@validate_input(PageSchema)
def get_all_post(page, **kwargs):
    page = Post.query.paginate(page=page, per_page=app.config["PER_PAGE"])
    posts = PostSchema().dump(page.items, many=True)
    total_count = page.total
    page_num = page.page
    return jsonify({
        "items": posts,
        "total_items": total_count,
        "page": page_num,
        "items_per_page": app.config["PER_PAGE"]
    })


@app.get("/post/<int:post_id>")
@check_post_exist
def get_one_post(*, post, **kwargs):
    return PostSchema().jsonify(post)


@app.post("/post")
@jwt_guard
@validate_input(PostSchema)
def create_post(*args, user_id, body, tags, **kwargs):
    post = Post(user_id=user_id, body=body)
    for tag_dict in tags:
        if "id" in tag_dict:
            tag = Tag.query.get(tag_dict["id"])
            if tag is None:
                raise RecordNotFoundError(error_data=tag_dict)
            else:
                post.tags.append(tag)
        else:
            tag = Tag(name=tag_dict["name"])
            post.tags.append(tag)

    db.session.add(post)
    db.session.commit()

    return PostSchema().jsonify(post)


@app.put("/post/<int:post_id>")
@jwt_guard
@validate_input(PostSchema, partial=True)
@check_post_exist
def update_post(user_id, post: Post, body=None, tags=None, **kwargs):
    if user_id != post.user_id:
        raise ForbiddenAccessError(error_data=post)

    new_tags = []
    if tags is not None:
        for tag_dict in tags:
            if "id" in tag_dict:
                tag: Tag = Tag.query.get(tag_dict["id"])
                if tag is None:
                    raise RecordNotFoundError(error_data=tag_dict)
                else:
                    if "name" in tag_dict:
                        tag.name = tag_dict["name"]
                    new_tags.append(tag)
            else:
                tag = Tag(name=tag_dict["name"])
                new_tags.append(tag)
        post.tags = new_tags

    if body is not None:
        post.body = body
    db.session.commit()
    return PostSchema().jsonify(post)


@app.delete("/post/<int:post_id>")
@jwt_guard
@check_post_exist
def delete_post(user_id, post, **kwargs):
    if post.user_id != user_id:
        raise ForbiddenAccessError(
            error_data={"post_id": post.id, "user_id": user_id})
    db.session.delete(post)
    db.session.commit()

    return PostSchema().jsonify(post)
