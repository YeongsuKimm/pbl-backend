import json
from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
import pandas as pd
from model.stroke import StrokeModel

stroke_api = Blueprint('stroke_api', __name__, url_prefix='/api/stroke')
api = Api(stroke_api)
class StrokeAPI:
    class _Predict(Resource):
        def post(self):
            if request.is_json:
                body = request.get_json()
                # Check for required fields and format validation
                required_fields = ['age', 'gender', 'hypertension', 'heart_disease', 'ever_married', 
                                   'work_type', 'Residence_type', 'avg_glucose_level', 'bmi']
                for field in required_fields:
                    if field not in body:
                        return {'message': f'{field} is missing in the request body'}, 400
                
                # Instantiate the StrokeModel and predict stroke probability
                stroke_model = StrokeModel.get_instance("./healthcare-dataset-stroke-data.csv")
                stroke_probability = stroke_model.predict_stroke_probability(body)
                
                return make_response(jsonify({'stroke_probability': stroke_probability}), 200)
            else:
                return {'message': 'Invalid JSON data provided'}, 400

    api.add_resource(_Predict, '/predict')

