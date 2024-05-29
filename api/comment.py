import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response, make_response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.comments import Comment
from model.users import Vid


comment_api = Blueprint('comment_api', __name__, url_prefix='/api/comment')
api = Api(comment_api)

class commentAPI:        
    class _ReadComment(Resource): 
        """
        GET Request (args: videoID): Returns all the comments that belong to a certain video
        POST Request (args: uid, playlist name): Attempts to add a new comment to the linked to the specified video
        """
        def get(self, vid) :
            video = Vid.query.filter_by(_videoID=vid).first() 
            comments = Comment.query.all() # gets all the comments from the database
            matchingComments = [] # creates an empty list to later add matching comments (comments that belong with the specified video)
            for comment in comments: 
                if(comment.getVideoID() == vid):
                    matchingComments.append(comment) # iterates through all the comments and adds the ones that belong with the specified video ID
            data = [] # an empty list for response data
            for comment in matchingComments: # adds the comments into a readable format to return as the response
                com = {
                    "comment": comment.getComment(),
                    "user": comment.getUser()
                }
                data.append(com)
            return jsonify(data)
        
        
    class _CRUD(Resource):
        def post(self):
            body = request.get_json()
            comment = body.get('comment') # retrieves the comment and the video ID of which the commented was posted from
            videoID = body.get('videoID')
            uid = body.get('uid') # retrieves the user ID that posted the comment
            
            com = Comment(comment, videoID, uid) # creates a new comment instance object
            com.create() # adds that newly created object into the database
            return jsonify(com.read()) # returns the successfully uploaded comment
            
    api.add_resource(_CRUD, '/')
    api.add_resource(_ReadComment, '/<int:vid>')