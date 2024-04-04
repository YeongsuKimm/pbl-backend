# Importing necessary libraries for data manipulation and Flask RESTful API creation
import pandas as pd
import numpy as np
from flask_restful import Api, Resource
from flask import Blueprint, request
from joblib import load

# Load the machine learning model from a joblib file
# Replace 'happiness_model.joblib' with the actual file name of your saved model
model = load('./api/happiness_model.joblib')

# Initialize a Flask Blueprint for the API, setting its name, import name, and URL prefix
happiness_api = Blueprint('happiness_api', __name__, url_prefix='/api/happiness')

# Create an API object to handle the API requests
api = Api(happiness_api)

# Define a class for the API that will handle POST requests for happiness score predictions
class happinessAPI:
    class _Predict(Resource):
        def post(self):
            # Retrieve JSON data sent from the frontend
            body = request.get_json()
            
            # Check if any data is received
            if body is not None:
                # Convert the received JSON data into a pandas DataFrame
                # and rename the columns to match the model's expected input
                data = pd.DataFrame([body])
                data = data.rename(columns={
                    "freedom": "Freedom to make life choices",
                    "lifespan": "Healthy life expectancy at birth",
                    "money": "Log GDP per capita",
                    "social": "Social support",
                    "location": "loc_encoded"
                })

                # Use the loaded model to predict the happiness score based on the input data
                # model.predict returns a numpy array, so we get the first element ([0]) as the score
                score = model.predict(data)[0]
                # Return the predicted score and a 200 OK status to the client
                return {'score': score}, 200
            else:
                # If no data was provided in the request, return an error message and a 400 Bad Request status
                return {'message': 'No data provided'}, 400
    
    # Register the prediction endpoint with the Flask API to handle POST requests at '/predict'
    api.add_resource(_Predict, '/predict')
