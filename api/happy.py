import pandas as pd
import numpy as np

from flask_restful import Api, Resource
from flask import Blueprint, request
from joblib import load

#Load the ML model: replace the file name with whatever yours is
model = load('./api/happiness_model.joblib')

#Initialize Flask API endpoint blueprint
happiness_api = Blueprint('happiness_api', __name__, url_prefix='/api/happiness')
api = Api(happiness_api)

#Use a post request to take data from the frontend as a JSON, then return output value
class happinessAPI:
    class _Predict(Resource):
        def post(self):
            #Get data from frontend
            body = request.get_json()
            
            if body is not None:
                #Convert frontend JSON output to a pandas dataframe
                data = pd.DataFrame([body])
                data = data.rename(columns={"freedom":"Freedom to make life choices","lifespan":"Healthy life expectancy at birth","money":"Log GDP per capita","social":"Social support","location":"loc_encoded"})
    
                #Predict and return the happiness score (model.predict returns a 1-element array so we need to take a slice)
                score = model.predict(data)[0]
                return {'score': score}, 200
            else:
                return {'message': 'No data provided'}, 400
    
    #Add endpoint resource for this method
    api.add_resource(_Predict, '/predict')