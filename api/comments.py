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
    def get(self):
            # Fetch comments from the database
            
            comments = Comment.query.all()
            
            # Convert comments to JSON-ready format
            json_ready = [{'UID': comment.uid, 'Restaurant': comment.restaurant, 'Rating': comment.rating} for comment in comments]
            print(json_ready)
            return make_response(json_ready,200)
        # except Exception as e:
        #     return make_response({'message': 'Failed to fetch comments', 'error': str(e)}, 500)
    

    def post(self):
        try:
            data = request.get_json()
            text = data.get('rating')
            if not text:
                return make_response({'message': 'Text is required for comment'}, 400)
            restaurant = data.get('restaurant')
            uid = data.get('uid')
            new_comment = Comment(uid=uid,restaurant=restaurant,rating=text)
            print(new_comment)
            new_comment.create()
            return make_response({'message': 'Comment submitted successfully'}, 200)
        except Exception as e:
            return {'message': 'Failed to submit comment', 'error': str(e)}, 500

api.add_resource(CommentAPI, '/')
