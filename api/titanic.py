import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response, make_response

from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
import os
import numpy as np
import pandas as pd
from model.titanic import * 


titanic_api = Blueprint('titanic_api', __name__, url_prefix='/api/titanic')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(titanic_api)

class TitanicAPI:        
    class _Predict(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self):
            ''' Read data for json body '''
            if request.is_json:
                body = request.get_json()
                ''' Avoid garbage in, error checking '''
                name = body.get('name')
                if name is None or not isinstance(name, str):
                    return {'message': f'name is missing or in the wrong format'}, 400
                
                pclass = body.get("pclass")
                if pclass is None or not isinstance(pclass, int):
                    return {'message': f'pclass is missing or in the wrong format'}, 400
                
                sex = body.get("sex")
                if sex is None or sex not in ['male', 'female']:
                    return {'message': f'sex is missing or in the wrong format'}, 400
                
                age = body.get("age")
                if age is None or not isinstance(age, int):
                    return {'message': f'age is missing or in the wrong format'}, 400
                
                sibsp = body.get("sibsp")
                if sibsp is None or not isinstance(sibsp, int):
                    return {'message': f'sibsp is missing or in the wrong format'}, 400
                
                parch = body.get("parch")
                if parch is None or not isinstance(parch, int):
                    return {'message': f'parch is missing or in the wrong format'}, 400
                
                fare = body.get("fare")
                if fare is None or not isinstance(fare, int):
                    return {'message': f'fare is missing or in the wrong format'}, 400
                
                embarked = body.get("embarked")
                if embarked is None or embarked not in ['S', 'C', 'Q']:
                    return {'message': f'embarked is missing or in the wrong format'}, 400
                
                alone = body.get("alone")
                if alone is None or alone not in ['true', 'false']:
                    return {'message': f'alone is missing or in the wrong format'}, 400
                else:
                    if(alone == "True"):
                        alone = True
                    else:
                        alone = False

                passenger = pd.DataFrame({
                    'name': [name],
                    'pclass': [pclass], # 2nd class picked as it was median, bargains are my preference, but I don't want to have poor accomodations
                    'sex': [sex],
                    'age': [age],
                    'sibsp': [sibsp], # I usually travel with my wife
                    'parch': [parch], # currenly I have 1 child at home
                    'fare': [fare], # median fare picked assuming it is 2nd class
                    'embarked': [embarked], # majority of passengers embarked in Southampton
                    'alone': [alone] # travelling with family (spouse and child))
                })
                results = prediction(passenger)
                
                return make_response(jsonify(results), 200)
            else:
                return {'message': 'invalid'}, 400
            
    api.add_resource(_Predict, '/predict')
    