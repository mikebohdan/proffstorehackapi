from flask_restful import Resource, marshal_with, fields, abort, reqparse
from app import db
from sqlalchemy import and_
from flask import g
from app.models import Comment, User, Project
from .auth import login_required

comment_fields = {
    "id": fields.Integer,
    "text": fields.String,
    "url": fields.Url('comment', absolute=True)
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('text', type=str)
parser.add_argument('task_id', type=int)


class Comment(Resource):
    decorators = [login_required]

    @marshal_with(comment_fields)
    def get(self, id):
        comment = db.session.query(Comment).filter(Comment.id == id).first()
        if not comment:
            return abort(404, message="Comment does not exist")
        return comment

    def delete(self, id):
        user_id = db.session.query(User).filter(User.id == g.user['id']).first()
        comment = db.session.query(Comment).filter(Comment.id == id).first()
        if not comment:
            return abort(403, message="Comment does not exist or you do not have access")
        db.session.delete(comment)
        db.session.commit()
        return {}, 204

    @marshal_with(comment_fields)
    def put(self, id):
        parsed = parser.parse_args()
        comment = db.session.query(Comment).filter(Comment.id == id).first()
        if not comment:
            return abort(403, message="Comment does not exist or you do not have access")
        comment.description = parsed['text']
        db.session.add(comment)
        db.session.commit()
        return comment, 201


class CommentList(Resource):
    decorators = [login_required]

    @marshal_with(comment_fields)
    def get(self):
        comments = db.session.query(Comment).all()
        return comments

    @marshal_with(comment_fields)
    def post(self):
        parsed = parser.parse_args()
        # user_id = db.session.query(User).filter(User.id == g.user['id']).first()
        comment = Comment(name=parsed['name'], description=parsed['text'], project_id=parsed['task_id'])
        task_comments = Comment.comments(comment.id, parsed['task_id'])
        db.session.add(task_comments)
        db.session.add(comment)
        db.session.commit()
        return comment, 201
