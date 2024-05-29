import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)
'''
Most of this was just a template that I used, I added some stuff like account deletion
'''
class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password and dob
            email = body.get('email')
            if email is None or "@" not in email:
                return {'message': f'Email is missing or in the wrong format'}, 400
            password = body.get('password')
            dob = body.get('dob')
            ''' #1: Key code block, setup USER OBJECT '''
            print(dob)
            preferences = body.get("preferences")
            uo = User(name=name, uid=uid, email=email, preferences=preferences)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.set_password(password)
            # convert to date type
            if dob is not None:
                try:
                    uo.dob = datetime.strptime(dob, '%m-%d-%Y').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
            
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        @token_required
        def get(self, current_user): # Read Method
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        

    class _Update(Resource):
        def post(self):
            body = request.get_json()
            uid = body.get('uid')
            print(uid)
            if uid is None:
                return {'message': f'User ID missing'}, 400
            email = body.get('email')
            print(email)
            if email is None or "@" not in email:
                return {'message': f'Email is blank or has an invalid format'}, 400
            user = User.query.filter_by(_uid=uid).first()
            print(user)
            if user:
                try:
                    user.update_email(email)
                    return jsonify(user.read())
                except Exception as e:
                    return {
                        "error": "Something went wrong",
                        "message": str(e)
                    }, 500
        def delete(self):
            '''done by me'''
            body = request.get_json()
            uid = body.get('uid')
            user = User.query.filter_by(_uid=uid).first()
            
            if user:
                if user.is_admin():
                    try:
                        user.delete()
                        return {f'{uid} has been deleted'}
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                

    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                ''' Get Data '''
                uid = body.get('uid')
                if uid is None:
                    return {'message': f'User ID is missing'}, 400
                password = body.get('password')
                
                ''' Find user '''
                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 401
                if user:
                    try:
                        token = jwt.encode(
                            {"_uid": user._uid, "role": user.role},
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        resp = Response("Authentication for %s successful" % (user._uid))
                        resp.set_cookie("jwt", token,
                                max_age=3600,
                                secure=True,
                                httponly=True,
                                path='/',
                                samesite='None'  # This is the key part for cross-site requests

                                # domain="frontend.com"
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

    class _Playlist(Resource):
        def get(self): # Read Method
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready) 
            
        def post(self):
            body = request.get_json()
            uid = body.get('uid')
            name = body.get('name')
            users = User.query.all()
            usr = -1
            for user in users:
                if(user.read()["uid"] == uid):
                    usr = user
            if(usr == -1):
                print("user doesn't exist")
                return {
                    "message": "User doesn't exist"
                }
            if(name in list(usr.read()["playlists"].keys())):
                print("playlist already exists")
                return {
                    "message": "Playlist already exists"
                }
            else:
                usr.createPlaylist(name)
                return jsonify(usr.read())
        
        '''
        PUT method (Takes the body request as JSON)
            Body params -> User ID (uid), name, Video ID (vidID)
        
        usr = -1 is set to be a checking flag conditional
        
        Calls the updated playlist method with the specific user name and videoID 
            
        '''
        def put(self):
            # Get the body w/ the User ID, name, Video ID
            body = request.get_json()
            uid = body.get('uid')
            name = body.get('name')
            vidID = body.get('vidID')
            # Query all the users

            users = User.query.all()
            usr = -1
            for user in users:
                if(user.read()["uid"] == uid):
                    usr = user

            # Check if the user exists in the table, if it doesn't throw an error
            if(usr == -1):
                print("user doesn't exist")
                return {
                    "message": "User doesn't exist"
                }

            # Check in the users table, playlists column, name value if the video is in the playlist
            if(vidID in usr.read()["playlists"][name]):
                print("video already exists in playlist")
                return {
                    "message": "Video already exists"
                }
            else:
                # updatePlaylist method in the model
                usr.updatePlaylist(name, int(vidID))
                return jsonify(usr.read())
        
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(_Update, '/update')
    api.add_resource(_Playlist, '/playlist')