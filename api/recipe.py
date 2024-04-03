import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from auth_middleware import token_required
from model.recipe import Recipe 

recipe_api = Blueprint('recipe_api', __name__, url_prefix='/api/recipe')
api = Api(recipe_api)

class RecipeAPI:
    class _CRUD(Resource):
        def post(self):
            if request.is_json:
                data = request.get_json()
                print("data")
                print(data)
                # Extract data from the request body\
                print(data)
                recipe_name = data.get('recipeName')
                recipe_instructions = data.get('recipeInstructions')
                recipe_ingredients = data.get('recipeIngredients')
                recommended_supplies = data.get('recommendedSupplies')

            
                # Create a new Recipe object
                recipe = Recipe(
                    name=recipe_name,
                    instruction=recipe_instructions,
                    ingredients=recipe_ingredients,
                    supplies=recommended_supplies,
                )
                print(recipe.read())
                print('follow')
                # Save the recipe to the database
                ro = recipe.create()  # Assuming you have a save method in your Recipe model
                
                if ro:
                    return jsonify(ro.read())
                return {'message': 'Failed to upload recipe: '}, 500

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
