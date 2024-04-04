import json
from flask import Blueprint, request, jsonify, make_response  # Import necessary Flask modules
from flask_restful import Api, Resource  # Import Flask-RESTful modules for API and resource handling
import pandas as pd  # Import pandas for data manipulation
from model.stroke import StrokeModel  # Import the StrokeModel class for stroke prediction

# Initialize a Flask Blueprint for the stroke prediction API, setting its name and URL prefix
stroke_api = Blueprint('stroke_api', __name__, url_prefix='/api/stroke')
api = Api(stroke_api)  # Create an API object to handle the API requests

# Define a class for the Stroke API to handle prediction requests
class StrokeAPI:
    # Nested class for handling prediction operations
    class _Predict(Resource):
        # Method to handle POST requests for making stroke predictions
        def post(self):
            # Check if the incoming request is in JSON format
            if request.is_json:
                # Parse the JSON data from the request
                body = request.get_json()

                # Define the required fields for the stroke prediction model
                required_fields = ['age', 'gender', 'hypertension', 'heart_disease', 'ever_married', 
                                   'work_type', 'Residence_type', 'avg_glucose_level', 'bmi']
                # Check if all required fields are present in the request body
                for field in required_fields:
                    if field not in body:
                        # Return an error message if a required field is missing
                        return {'message': f'{field} is missing in the request body'}, 400
                
                # Instantiate the StrokeModel with the dataset path
                stroke_model = StrokeModel.get_instance("./healthcare-dataset-stroke-data.csv")
                # Use the stroke model to predict the probability of having a stroke based on the request data
                stroke_probability = stroke_model.predict_stroke_probability(body)
                
                # Return the stroke probability as a JSON response
                return make_response(jsonify({'stroke_probability': stroke_probability}), 200)
            else:
                # Return an error message if the request data is not in JSON format
                return {'message': 'Invalid JSON data provided'}, 400

    # Add the prediction resource to the API at the '/predict' endpoint
    api.add_resource(_Predict, '/predict')
