import json
from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_login import login_required
from werkzeug.security import check_password_hash
from model.comment import Comment
from __init__ import db, app

comments_api = Blueprint('comments_api', __name__, url_prefix='/api/comments')
api = Api(comments_api)
db.init_app(app)

class CommentAPI(Resource):
    @login_required
    def get(self):
        try:
            # Fetch comments from the database
            comments = Comment.query.all()
            # Convert comments to JSON-ready format
            json_ready = [{'UID': comment.uid, 'Restaurant': comment.restaurant, 'Rating': comment.rating} for comment in comments]
            return jsonify(json_ready), 200
        except Exception as e:
            return {'message': 'Failed to fetch comments', 'error': str(e)}, 500
    
    @login_required
    def post(self):
        try:
            data = request.get_json()
            text = data.get('text')
            if not text:
                return {'message': 'Text is required for comment'}, 400
            new_comment = Comment(text=text)
            db.session.add(new_comment)
            db.session.commit()
            return {'message': 'Comment submitted successfully'}, 201
        except Exception as e:
            return {'message': 'Failed to submit comment', 'error': str(e)}, 500

api.add_resource(CommentAPI, '/')
