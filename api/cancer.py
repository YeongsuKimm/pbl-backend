# Import necessary libraries
import pandas as pd  # Provides data structures and data analysis tools
import numpy as np   # Used for numerical computing

# Flask-RESTful is an extension for Flask that adds support for
# quickly building REST APIs. It is a lightweight abstraction that works with your existing ORM/libraries.
from flask_restful import Api, Resource  # Api handles the registration of the resources, Resource is what we create our endpoints from
from flask import Blueprint, request    # Blueprint is a way to organize a group of related views and other code, request is used to get data sent by the client
from joblib import load  # load is used to load a trained machine learning model from a file

# Load the ML model: replace 'cancer_model.joblib' with the path to your trained model file
model = load('./api/cancer_model.joblib')

# Initialize a Flask Blueprint. This is a way to organize your Flask app into components.
# Here, 'cancer_api' is the name of the Blueprint, and '/api/cancer' is the base URL path it will handle.
cancer_api = Blueprint('cancer_api', __name__, url_prefix='/api/cancer')
api = Api(cancer_api)  # Create an API object that will register the endpoints

# Define a class for the API endpoint. This will handle requests to predict cancer.
class cancerAPI:
    # Define a class for the prediction resource. It inherits from 'Resource' which means it can be used to handle HTTP requests.
    class _Predict(Resource):
        # Define the POST method which will be called when the API receives a POST request.
        def post(self):
            # Get JSON data sent from the frontend
            body = request.get_json()
            
            # Check if any data is received from the frontend
            if body is not None:
                # Convert the JSON data into a DataFrame which the model can understand
                data = pd.DataFrame([body])
                # Rename the columns of the DataFrame to match the model's expected input
                data = data.rename(columns={
                    "bareNuclei": "Bare Nuclei",
                    "epithelialCellSize": "Single Epithelial Cell Size",
                    "mitoses": "Mitoses",
                    "normalNucleoli": "Normal Nucleoli",
                    "clumpThickness": "Clump Thickness",
                    "cellSizeUniformity": "Uniformity of Cell Size",
                    "cellShapeUniformity": "Uniformity of Cell Shape"
                })

                # Use the model to predict the result based on the data provided and retrieve the first result from the array
                benign_proba, malignant_proba = model.predict_proba(data)[0]
                # Return the prediction score and HTTP status code 200 (OK)
                return {'benign': benign_proba, 'malignant': malignant_proba}, 200
            else:
                # If no data is provided, return a message and HTTP status code 400 (Bad Request)
                return {'message': 'No data provided'}, 400
    
    # Add the _Predict resource to the API endpoint at the URL '/predict'
    api.add_resource(_Predict, '/predict')

# Remember, to activate this API endpoint, you'll need to register the Blueprint with your Flask application object elsewhere in your code.
