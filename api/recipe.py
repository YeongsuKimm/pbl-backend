import json
import logging  # Import logging module for debugging
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from auth_middleware import token_required  # Middleware for handling token authentication
from model.recipe import Recipe  # Importing the Recipe class from the model module

# Setting up logging
logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG

# Setting up a Blueprint for the recipe API
recipe_api = Blueprint('recipe_api', __name__, url_prefix='/api/recipe')
api = Api(recipe_api)  # Creating an API object associated with the Blueprint

class RecipeAPI:
    class _CRUD(Resource):
        def post(self, recipe_id=None):
            logging.debug(f"Requesting to like recipe with ID: {recipe_id}")  # Debug statement
            if recipe_id:  # If recipe_id is provided, it means the like button was pressed
                try:
                    recipe = Recipe.query.get(recipe_id)
                    if not recipe:
                        return {'message': 'Recipe not found'}, 404
                    
                    recipe.likes += 1
                    recipe.update()  # Assuming there's an update method in Recipe class
                    return jsonify({'message': 'Recipe liked successfully', 'recipe_likes': recipe.likes}), 200
                except Exception as e:
                    logging.error(f"Error liking recipe: {e}")  # Log error
                    return {'message': f'Failed to like recipe: {str(e)}'}, 500
            else:  # If recipe_id is None, it means a new recipe is being created
                logging.debug("Requesting to create a new recipe")  # Debug statement
                if request.is_json:
                    data = request.get_json()
                    # Extracting fields from the JSON data
                    recipe_name = data.get('recipeName')
                    recipe_instructions = data.get('recipeInstructions')
                    recipe_ingredients = data.get('recipeIngredients')
                    recommended_supplies = data.get('recommendedSupplies')
                    userid = data.get('userid')  # Extracting userid from JSON data

                    # Creating a new Recipe object with the extracted data
                    recipe = Recipe(
                        userid=userid,  # Passing userid to the Recipe constructor
                        name=recipe_name,
                        instruction=recipe_instructions,
                        ingredients=recipe_ingredients,
                        supplies=recommended_supplies,
                    )

                    # Attempting to save the new recipe object to the database
                    ro = recipe.create()

                    # Checking if the recipe was successfully saved and returning the result
                    if ro:
                        return jsonify(ro.read())
                    return {'message': 'Failed to upload recipe'}, 500

                else:
                    logging.error("Request body is not in JSON format")  # Log error
                    return {'message': 'Request body must be in JSON format'}, 400

        def get(self, recipe_id=None):
            logging.debug(f"Requesting recipe with ID: {recipe_id}")  # Debug statement
            if recipe_id is None:
                recipes = Recipe.query.all()
                json_ready = [recipe.read() for recipe in recipes]
                return jsonify(json_ready)
            else:
                recipe = Recipe.query.get(recipe_id)
                if not recipe:
                    return {'message': 'Recipe not found'}, 404
                return jsonify({'recipe_likes': recipe.likes}), 200

        def put(self):
            try:
                body = request.get_json()
                recipe_id = body.get("recipe_id")
                recipe = Recipe.query.get(recipe_id)

                if not recipe:
                    return {'message': 'Recipe not found'}, 404

                recipe.like()  # Assuming there's an update method in Recipe class

                return jsonify({'message': 'Recipe updated successfully', 'recipe': recipe.read()}), 200
            except Exception as e:
                logging.error(f"Error updating recipe: {e}")  # Log error
                return {'message': f'Failed to update recipe: {str(e)}'}, 500

    api.add_resource(_CRUD, '/', '/<int:recipe_id>')
