# Import necessary libraries and modules
import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response, make_response, session
from flask_restful import Api, Resource  # For building REST APIs
from datetime import datetime
from auth_middleware import token_required  # Middleware for token-based authentication
import os
from flask_jwt_extended import jwt_required, get_jwt_identity  # For JWT operations

# Import User and College models from the model directory
from model.users import User
from model.colleges import College

# Initialize a Flask Blueprint for the user-related API endpoints
user_api = Blueprint('user_api', __name__, url_prefix='/api/users')
api = Api(user_api)  # Wrap the Blueprint with Flask-RESTful

# UserAPI class containing methods to interact with user data
class UserAPI(Resource):
    # This is the start of a blueprint for handling user actions in our web application, 
    # like logging in or editing user information.

    def post(self):
        # Here, we start handling a user logging in:
        body = request.get_json()  # We're getting data sent by the user, like their username or password.
        uid = body.get('uid')  # From that data, we specifically get the user's ID (a unique identifier).
        session['uid'] = uid  # We then remember this user ID so we know which user is logged in during their session.

class _Edit(Resource):
    def post(self):
        # Defining post to add new colleges to a user's list.
        # When a user wants to add a college, this part is activated.

        username = session.get('uid')  # We get the user's ID again to know who is trying to make the changes.
        user = User.query.filter_by(_uid=username).first()  # We look for the user in our database to get their information.
        
        if user is None:
            # If we can't find the user...
            return {'message': "Invalid user id"}, 400
        
        # We get the list of colleges that the user has saved.
        namelist = json.loads(user.college_list)
        
        # We find the colleges in the database that match the user's list.
        matching_colleges = College.query.filter(College.name.in_(namelist)).all()
        colleges_data = [college.read() for college in matching_colleges]  # We prepare the college information to be sent back to the user.
        json_data = jsonify(colleges_data)
        
        return json_data  # We send the information about the colleges back to the user.

    def get(self):
        # This is a tool for getting a list of all colleges.
        # When a user wants to see all colleges, this part is activated.

        all_colleges = College.query.all()  # We get every college from our database.
        colleges_data = [college.read() for college in all_colleges]  # We prepare the college information to be sent to the user.
        json_data = jsonify(colleges_data)
        return json_data  # We send the information about all colleges back to the user.

    def put(self):
        # This is a tool for updating the list of colleges a user has.
        # When a user wants to change their college list, this part is activated.

        username = session.get('uid')  # Again, we get the user's ID to know who is making the changes.
        user = User.query.filter_by(_uid=username).first()  # We find the user in our database.
        
        if user is None:
            # If we can't find the user, we tell them something went wrong.
            return {'message': "Invalid user id"}, 400
        
        namelist = json.loads(user.college_list)  # We get the current list of colleges that the user has.
        
        body = request.get_json()  # We get the new data sent by the user.
        selected_names = body.get('names', [])  # From that data, we extract the list of colleges they want to add.
        
        namelist += [elem for elem in selected_names if elem not in namelist]  # We add the new colleges to the user's list, making sure not to add duplicates.
        
        user.update_list(json.dumps(namelist))  # We save the updated list of colleges for the user in the database.

# This line makes our editing tools available in the web application under the web address ending in '/edit'.
api.add_resource(_Edit, '/edit')
