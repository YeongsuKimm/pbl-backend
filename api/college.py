import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response, make_response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
import os
from flask_jwt_extended import jwt_required, get_jwt_identity

from model.users import User
from model.colleges import College


