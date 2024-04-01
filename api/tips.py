import json, jwt
from flask import Blueprint, request, Flask, current_app, Response, make_response, jsonify

from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
import os
import numpy as np
import pandas as pd
from model.tips import * 
from model.tips2 import *


tips_api = Blueprint('tips_api', __name__, url_prefix='/api/tips')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(tips_api)

class TipsAPI:        
    class _Predict1(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): 
            ''' Read data for json body '''
            if request.is_json:
                body = request.get_json()
                ''' Avoid garbage in, error checking '''
                total_bill = round(float(body.get('total_bill')),2)
                if total_bill is None or not isinstance(total_bill, float):
                    return {'message': f'total_bill is missing or in the wrong format'}, 400
                
                sex = body.get("sex")
                if sex is None or sex not in ["Female", "Male"]:
                    return {'message': f'sex is missing or in the wrong format'}, 400
                
                smoker = body.get("smoker")
                if smoker is None or smoker not in ['Yes', 'No']:
                    return {'message': f'smoker is missing or in the wrong format'}, 400
                
                day = body.get("day")
                if day is None or day not in ["Thur", "Fri", "Sat", "Sun"]:
                    return {'message': f'day is missing or in the wrong format, we only except weekend days'}, 400
                
                time = body.get("time")
                if time is None or time not in ['Dinner', 'Lunch']:
                    return {'message': f'time is missing or in the wrong format'}, 400
                
                size = body.get("size")
                if size is None or size not in [1, 2, 3, 4, 5, 6]:
                    return {'message': f'size is missing or in the wrong format or is out of range from 1-6'}, 400
                

                customer = pd.DataFrame({
                    'total_bill': [total_bill],
                    'sex': [sex], # 2nd class picked as it was median, bargains are my preference, but I don't want to have poor accomodations
                    'smoker': [smoker],
                    'day': [day],
                    'time': [time], # I usually travel with my wife
                    'size': [size], # currenly I have 1 child at home
                })
                tipsModel = TipsModel.get_instance()

                
                results = round(float(tipsModel.predict_tip(customer)),2)
                print(type(round(float(results),2)))
                return make_response(jsonify(results), 200)
            else:
                return {'message': 'invalid'}, 400
            
    class _Predict2(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self):
            ''' Read data for json body '''
            if request.is_json:
                body = request.get_json()
                ''' Avoid garbage in, error checking '''
                total_bill = round(float(body.get('total_bill')),2)
                if total_bill is None or not isinstance(total_bill, float):
                    return {'message': f'total_bill is missing or in the wrong format'}, 400
                
                sex = body.get("sex")
                if sex is None or sex not in ["Female", "Male"]:
                    return {'message': f'sex is missing or in the wrong format'}, 400
                
                smoker = body.get("smoker")
                if smoker is None or smoker not in ['Yes', 'No']:
                    return {'message': f'smoker is missing or in the wrong format'}, 400
                
                day = body.get("day")
                if day is None or day not in ["Thur", "Fri", "Sat", "Sun"]:
                    return {'message': f'day is missing or in the wrong format, we only except weekend days'}, 400
                
                time = body.get("time")
                if time is None or time not in ['Dinner', 'Lunch']:
                    return {'message': f'time is missing or in the wrong format'}, 400
                
                size = body.get("size")
                if size is None or size not in [1, 2, 3, 4, 5, 6]:  
                    return {'message': f'size is missing or in the wrong format or is out of range from 1-6'}, 400
                

                customer = pd.DataFrame({
                    'total_bill': [total_bill],
                    'sex': [sex], # 2nd class picked as it was median, bargains are my preference, but I don't want to have poor accomodations
                    'smoker': [smoker],
                    'day': [day],
                    'time': [time], # I usually travel with my wife
                    'size': [size], # currenly I have 1 child at home
                })
                tipsModel = TipsModel2.get_instance()
                
                results = round(float(tipsModel.predict_tip(customer)),2)
                print(type(round(float(results),2)))
                return make_response(jsonify(results), 200)
        
            else:
                return {'message': 'invalid'}, 400
                    
    
    api.add_resource(_Predict1, '/predict1')
    api.add_resource(_Predict2, '/predict2')
    
# {
#     "total_bill": 11.11,
#     "sex": "Male",
#     "smoker": "Yes",
#     "day": "Thur",
#     "time": "Dinner",
#     "size": 3
# }