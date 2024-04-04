import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response, make_response, session
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
import os
from flask_jwt_extended import jwt_required, get_jwt_identity

from model.users import User
from model.colleges import College

user_api = Blueprint('user_api', __name__, url_prefix='/api/users')
api = Api(user_api)


#PLEASE NOTE - This was designed as an extension to UserAPI, rather than its own module, since it requires session storage.
#Do NOT integrate this as its separate API.

class UserAPI: #replace with your own UserAPI instance
    
    #This should go in security login function
    body = request.get_json()
    uid = body.get('uid')
    session['uid'] = uid

    #PUT IN UserAPI
    class _Edit(Resource):
            # JSON of all colleges in the user's list
            def post(self):
                #Get uid of the current session
                username = session.get('uid')
                user = User.query.filter_by(_uid=username).first()
                
                if user is None:
                    #error handling
                    return {'message': f"Invalid user id"}, 400
                
                if user:
                    #Load user's college list - NEEDS COLUMN college_list IN users.py (see below)
                    namelist = json.loads(user.college_list)
                    
                    #Find all matching records
                    matching_colleges = College.query.filter(College.name.in_(namelist)).all()
                    colleges_data = [college.read() for college in matching_colleges]
                    json_data = jsonify(colleges_data)
                    
                    #Return all matching records as JSON
                    return json_data

            # JSON of whole Colleges dataset
            def get(self):
                # Query the database to retrieve all colleges
                all_colleges = College.query.all()

                # Convert the queried data to a list of dictionaries
                colleges_data = [college.read() for college in all_colleges]

                # Convert data to JSON format
                json_data = jsonify(colleges_data)

                # Return JSON response to the frontend
                return json_data

            # Append selected colleges to user list if they are not already there
            def put(self):
                #Get uid of the current session
                username = session.get('uid')
                user = User.query.filter_by(_uid=username).first()
                
                if user is None:
                    #error handling
                    return {'message': f"Invalid user id"}, 400
                
                if user:
                    #Load user's college list
                    namelist = json.loads(user.college_list)
                    
                    body = request.get_json() #Get JSON containing list of user selections as JS Array
                    selected_names = body.get('names', []) #Get selections as Python list
                    
                    #Add new elements to namelist
                    namelist += [elem for elem in selected_names if elem not in namelist]
                    
                    #Update user list - NEEDS CORRESPONDING FUNCTION IN users.py (see below)
                    user.update_list(json.dumps(namelist))
                    
                
            
    api.add_resource(_Edit, '/edit')
    
    
#Note that college_list is the stringified version of a Python list containing all the user's selections. I won't change user.py as requested, but here it is:

'''
    _college_list = db.Column(db.String(255), unique=False, nullable=False)
    @property
    def college_list(self):
        return self._college_list
    
    @college_list.setter
    def college_list(self, college_list):
        self._college_list = college_list
        
    def __init__(self, name, uid, email, password="123qwerty", dob=datetime.today(), college_list='[]'):
        (all properties)
''' #and add all other requisite lines needed for a SQLite db column

#Also add this function to users.py SQLite model:
'''
def update_list(self, list=""):
        self.college_list = list
        db.session.commit()
        print(self.email)
        return self
'''