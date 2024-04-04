# Import necessary libraries and modules
import json, jwt  # For handling JSON data and JSON Web Tokens (JWT)
from flask import Blueprint, request, jsonify, current_app, Response, make_response, session  # Flask framework imports
from flask_restful import Api, Resource  # For creating REST APIs with Flask
from datetime import datetime  # For handling date and time operations
from auth_middleware import token_required  # Custom middleware for token-based authentication
import os  # For accessing operating system functionalities
from flask_jwt_extended import jwt_required, get_jwt_identity  # Extended functionalities for handling JWT in Flask

# Importing User and College models from the model directory to interact with the database
from model.users import User
from model.colleges import College

# Initialize a Flask Blueprint for the user-related API endpoints with a URL prefix
user_api = Blueprint('user_api', __name__, url_prefix='/api/users')
api = Api(user_api)  # Create a Flask-RESTful API object by wrapping the Blueprint

# Define a class for User API, inheriting from Resource to use with Flask-RESTful
class UserAPI(Resource):
    # Nested class for handling security-related operations such as user authentication
    class _Security(Resource):
        # POST method for authenticating users and returning JWT
        def post(self):
            try:
                # Extract JSON data from the request
                body = request.get_json()
                # Retrieve user ID from the request data
                uid = body.get('uid')
                # Store user ID in session for tracking user's session
                session['uid'] = uid  

                # Ensure body contains data
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400

                # Get user ID and password from request data for authentication
                uid = body.get('uid')
                if uid is None:
                    return {'message': f'User ID is missing'}, 400
                password = body.get('password')

                # Retrieve user from database using user ID and verify password
                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 401

                # If user is authenticated, generate and return a JWT
                if user:
                    try:
                        token = jwt.encode(
                            {"_uid": user._uid, "role": user.role},
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        # Create a response object to set cookie with JWT
                        resp = Response("Authentication for %s successful" % (user._uid))
                        resp.set_cookie("jwt", token,
                                max_age=3600,  # Token expiration time
                                secure=True,  # HTTPS only
                                httponly=True,  # Prevent access via JavaScript
                                path='/',
                                samesite='None'  # Necessary for cross-site requests
                                )
                        return resp
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                return {
                    "message": "Error fetching auth token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 404
            except Exception as e:
                return {
                        "message": "Something went wrong!",
                        "error": str(e),
                        "data": None
                }, 500

    # Nested class for editing college data associated with a user
    class _Edit(Resource):
        # POST method to add new colleges to a user's list
        def post(self):
            # Retrieve the user's ID from the session to identify the user making the request
            username = session.get('uid')
            # Query the database for the user's record using the user ID
            user = User.query.filter_by(_uid=username).first()
            
            if user is None:
                return {'message': "Invalid user id"}, 400
            
            # Decode the JSON string of the user's college list into a Python list
            namelist = json.loads(user.college_list)
            # Query the database for colleges that match the names in the user's list
            matching_colleges = College.query.filter(College.name.in_(namelist)).all()
            # Convert the query results to a JSON-serializable format
            colleges_data = [college.read() for college in matching_colleges]
            json_data = jsonify(colleges_data)
            
            return json_data  # Return the JSON data of the colleges

        # GET method to retrieve a list of all colleges from the database
        def get(self):
            # Query the database for all college records
            all_colleges = College.query.all()
            # Convert each college record to a JSON-serializable format
            colleges_data = [college.read() for college in all_colleges]
            json_data = jsonify(colleges_data)
            
            return json_data  # Return the JSON data of all colleges

        # PUT method to update the college list associated with a user
        def put(self):
            # Retrieve the user's ID from the session
            username = session.get('uid')
            # Query the database for the user's record
            user = User.query.filter_by(_uid=username).first()
            
            if user is None:
                return {'message': "Invalid user id"}, 400
            
            # Decode the JSON string of the user's current college list into a Python list
            namelist = json.loads(user.college_list)
            # Extract data from the request's JSON body
            body = request.get_json()
            # Get the list of college names from the request data
            selected_names = body.get('names', [])
            
            # Update the user's college list by adding new names, avoiding duplicates
            namelist += [elem for elem in selected_names if elem not in namelist]
            # Update the user's record in the database with the new college list
            user.update_list(json.dumps(namelist))

    # Register the _Edit class with the API to handle requests at the '/edit' endpoint
    api.add_resource(_Edit, '/edit')
    # Register the _Security class with the API to handle requests at the '/security' endpoint
    api.add_resource(_Security, '/security')
