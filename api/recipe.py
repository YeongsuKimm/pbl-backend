# Importing necessary libraries and modules
import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from auth_middleware import token_required  # Middleware for handling token authentication
from model.recipe import Recipe  # Importing the Recipe class from the model module

# Setting up a Blueprint for the recipe API
recipe_api = Blueprint('recipe_api', __name__, url_prefix='/api/recipe')
api = Api(recipe_api)  # Creating an API object associated with the Blueprint

class RecipeAPI:
    # Inner class for CRUD operations related to recipes
    class _CRUD(Resource):
        # Method to handle POST requests for creating new recipes
        def post(self):
            # Check if the incoming request is in JSON format
            if request.is_json:
                # Extracting JSON data from the request
                data = request.get_json()
                # Debug print statements to check the received data
                print("data")
                print(data)
                
                # Extract individual fields from the JSON data
                recipe_name = data.get('recipeName')
                recipe_instructions = data.get('recipeInstructions')
                recipe_ingredients = data.get('recipeIngredients')
                recommended_supplies = data.get('recommendedSupplies')

                # Creating a new Recipe object with the extracted data
                recipe = Recipe(
                    name=recipe_name,
                    instruction=recipe_instructions,
                    ingredients=recipe_ingredients,
                    supplies=recommended_supplies,
                )
                # Debug print to check the recipe object's read method output
                print(recipe.read())
                print('follow')
                
                # Attempting to save the new recipe object to the database
                ro = recipe.create()  # Assuming there's a create method in Recipe class
                
                # Checking if the recipe was successfully saved and returning the result
                if ro:
                    return jsonify(ro.read())
                # Returning an error message if the recipe saving failed
                return {'message': 'Failed to upload recipe: '}, 500

            # Returning an error message if the request data is not in JSON format
            else:
                return {'message': 'Request body must be in JSON format'}, 400

        # Method to handle GET requests for retrieving all recipes
        def get(self):
            # Querying all recipe entries from the database
            recipes = Recipe.query.all()
            # Converting each recipe object to a JSON-ready format using the read method
            json_ready = [recipe.read() for recipe in recipes]
            # Returning the list of recipes in JSON format
            return jsonify(json_ready)

        # Placeholder for additional CRUD operations (PUT, DELETE, etc.)

    # Adding the CRUD class as a resource to the API at the root endpoint
    api.add_resource(_CRUD, '/')
    