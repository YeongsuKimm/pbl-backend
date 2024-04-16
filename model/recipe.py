""" database dependencies to support sqliteDB examples """
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


""" Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along """


# Define the Recipe class to manage actions in 'recipes' table
class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), nullable=False)
    _instruction = db.Column(db.String(255), nullable=False)
    _supplies = db.Column(db.String(255), nullable=False)
    _ingredients = db.Column(db.String(255), nullable=False)

    def __init__(self, name, instruction, supplies, ingredients):
        self._name = name
        self._instruction = instruction
        self._supplies = supplies
        self._ingredients = ingredients

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def instruction(self):
        return self._instruction
    
    @instruction.setter
    def instruction(self, instruction):
        self._instruction = instruction
        
    @property
    def supplies(self):
        return self._supplies
    
    @supplies.setter
    def supplies(self, supplies):
        self._supplies = supplies

    @property
    def ingredients(self):
        return self._ingredients
    
    @ingredients.setter
    def ingredients(self, ingredients):
        self._ingredients = ingredients

    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "instruction": self.instruction,
            "supplies": self.supplies,
            "ingredients": self.ingredients,
        }


"""Database Creation and Testing """


# Builds working data for testing
def initRecipes():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester records for table"""
        recipe1 = Recipe(
            name='Pizza',
            instructions='''1. In a large mixing bowl, combine warm water, yeast, and sugar. Let it sit for 5-10 minutes until foamy.
2. Add flour, salt, and olive oil to the yeast mixture. Mix until a dough forms.
3. Knead the dough on a floured surface for about 5-7 minutes until smooth and elastic.
4. Place the dough in an oiled bowl, cover with a clean towel, and let it rise for 1-1.5 hours until doubled in size.
5. Preheat the oven to its highest temperature (usually around 500°F or 260°C) and place a pizza stone or baking sheet inside to heat.
6. Punch down the dough and divide it into two balls for two medium-sized pizzas.
7. On a floured surface, roll out each dough ball into a circle of desired thickness.
8. Transfer the dough to a pizza peel or parchment-lined baking sheet.
9. Spread tomato sauce over the dough, leaving a border for the crust.
10. Sprinkle shredded mozzarella cheese and desired toppings over the sauce.
11. Carefully slide the pizza onto the preheated pizza stone or baking sheet in the oven.
12. Bake for 10-12 minutes or until the crust is golden and the cheese is bubbly and melted.
13. Remove from the oven, let it cool slightly, slice, and enjoy your homemade pizza!''',
            supplies='''- Large mixing bowl
- Clean towel
- Pizza stone or baking sheet
- Rolling pin
- Pizza peel (optional) 
- Parchment paper''',
            ingredients='''- 1 ½ cups warm water (about 110°F or 43°C)
- 1 packet (2 ¼ teaspoons) active dry yeast
- 1 teaspoon sugar
- 4 cups all-purpose flour
- 1 teaspoon salt
- 2 tablespoons olive oil
- 1 cup tomato sauce
- 2 cups shredded mozzarella cheese
- Toppings of your choice (e.g., pepperoni, sliced bell peppers, onions, mushrooms)'''
)

        recipes = [recipe1]

        """Builds sample user/note(s) data"""
        for recipe in recipes:
            try:
                recipe.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {recipe.name}")

# Other parts of the code (User class, initUsers function, etc.) remain unchanged.


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
