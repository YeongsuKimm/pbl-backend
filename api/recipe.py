import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from auth_middleware import token_required
from model.users import Recipe 

recipe_api = Blueprint('recipe_api', __name__, url_prefix='/api/recipe')
api = Api(recipe_api)

class RecipeAPI:
    class _CRUD(Resource):
        @token_required
        def post(self, current_user):
            if request.is_json:
                data = request.get_json()
                # Extract data from the request body
                recipe_name = data.get('recipeName')
                recipe_instructions = data.get('recipeInstructions')
                recipe_ingredients = data.get('recipeIngredients')
                recommended_supplies = data.get('recommendedSupplies')
                recipe_thumbnail = request.files.get('recipeThumbnail')
                category = data.get('category')  # New attribute

                # Check if all required fields are present
                if not (recipe_name and recipe_instructions and recipe_ingredients and recommended_supplies and recipe_thumbnail and category):
                    return {'message': 'All fields are required'}, 400

                # Save the recipe thumbnail to a designated directory
                if recipe_thumbnail.filename == '':
                    return {'message': 'No file selected for recipe thumbnail'}, 400

                # Here you can add code to save the thumbnail file and get its name/path

                # Create a new Recipe object
                recipe = Recipe(
                    name=recipe_name,
                    instructions=recipe_instructions,
                    ingredients=recipe_ingredients,
                    supplies=recommended_supplies,
                    thumbnail=recipe_thumbnail,  # Replace with the name/path of the thumbnail file
                    category=category 
                )

                # Save the recipe to the database
                try:
                    recipe.save()  # Assuming you have a save method in your Recipe model
                    return {'message': 'Recipe uploaded successfully'}, 201
                except Exception as e:
                    return {'message': f'Failed to upload recipe: {str(e)}'}, 500

            else:
                return {'message': 'Request body must be in JSON format'}, 400

        def get(self):
            # Retrieve all recipes from the database
            recipes = Recipe.query.all()
            # Convert recipes to JSON-ready format
            json_ready = [recipe.read() for recipe in recipes]
            # Return JSON response
            return jsonify(json_ready)

        # Implement other CRUD operations as needed

    api.add_resource(_CRUD, '/')
