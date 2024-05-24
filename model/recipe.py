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
    _userid = db.Column(db.String(255), nullable=False)
    _name = db.Column(db.String(255), nullable=False)
    _instruction = db.Column(db.String(255), nullable=False)
    _supplies = db.Column(db.String(255), nullable=False)
    _ingredients = db.Column(db.String(255), nullable=False)
    _thumbnail = db.Column(db.String(255), nullable=True)
    _likes = db.Column(db.Integer, default=0)

    def __init__(self, userid, name, instruction, supplies, ingredients, thumbnail=None, likes=0):
        self._userid = userid
        self._name = name
        self._instruction = instruction
        self._supplies = supplies
        self._ingredients = ingredients
        self._thumbnail = thumbnail
        self._likes = likes

    @property
    def userid(self):
        return self._userid

    @userid.setter
    def userid(self, userid):
        self._userid = userid

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

    @property
    def thumbnail(self):
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, thumbnail):
        self._thumbnail = thumbnail
    @property
    def likes(self):
        return self._likes

    @likes.setter
    def likes(self, value):
        self._likes = value

    def like(self):
        self._likes += 1
        db.session.commit()

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        return {
            "id": self.id,
            "userid": self.userid,
            "name": self.name,
            "instruction": self.instruction,
            "supplies": self.supplies,
            "ingredients": self.ingredients,
            "thumbnail": self.thumbnail,
            "likes": self.likes
        }

# Database Creation and Testing
def initRecipes():
    with app.app_context():
        db.create_all()
        recipe1 = Recipe(
            userid="Tony Stark",
            name='Classic Lasagna',
            instruction='Layer lasagna sheets with ricotta cheese, marinara sauce, and ground beef. Repeat layers and top with mozzarella cheese. Bake in the oven until bubbly and golden.',
            supplies='Baking dish, mixing bowls, spatula, pot',
            ingredients='1 package lasagna sheets, 2 cups ricotta cheese, 2 cups marinara sauce, 1 pound ground beef, 2 cups shredded mozzarella cheese',
            thumbnail='https://thecozycook.com/wp-content/uploads/2022/04/Lasagna-Recipe.jpg',
            likes=4  # Initial likes count
        )
        recipe2 = Recipe(
            userid="Gordon Ramsey",
            name='BBQ Pulled Pork Sandwiches',
            instruction='Slow-cook pork shoulder with BBQ sauce until tender. Shred the pork and serve on sandwich buns with coleslaw.',
            supplies='Slow cooker, tongs, serving platter',
            ingredients='Pork shoulder, BBQ sauce, sandwich buns, coleslaw',
            thumbnail='https://www.thespeckledpalate.com/wp-content/uploads/2023/07/The-Speckled-Palate-BBQ-Pulled-Pork-Sandwiches-Photo-1365x2048.jpg',
            likes=12  # Initial likes count
        )
        recipe3 = Recipe(
            userid="Flopper",
            name='Chicken Alfredo Pasta',
            instruction='Cook fettuccine pasta until al dente. Sauté chicken breast slices in butter. Toss cooked pasta with Alfredo sauce and chicken. Serve with grated Parmesan cheese.',
            supplies='Pot, skillet, colander, mixing bowls, spatula',
            ingredients='Fettuccine pasta, chicken breast, butter, Alfredo sauce, Parmesan cheese',
            thumbnail='https://thecozycook.com/wp-content/uploads/2022/08/Chicken-Alfredo-Pasta-1.jpg',
            likes=85 # Initial likes count
        )
        recipe4 = Recipe(
            userid="Tony Stark",
            name='Teriyaki Salmon',
            instruction='Marinate salmon fillets in teriyaki sauce. Grill or bake until cooked through. Serve with steamed rice and stir-fried vegetables.',
            supplies='Grill pan or baking dish, serving platter, pot, spatula',
            ingredients='Salmon fillets, teriyaki sauce, steamed rice, assorted vegetables',
            thumbnail='https://natashaskitchen.com/wp-content/uploads/2016/01/Teriyaki-Salmon-Recipe-4.jpg',
            likes=50  # Initial likes count
        )
        recipe5 = Recipe(
            userid="Mickey Mouse",
            name='Vegetable Stir-Fry',
            instruction='Stir-fry mixed vegetables (such as bell peppers, broccoli, carrots) in a hot pan with soy sauce and ginger. Serve over cooked rice or noodles.',
            supplies='Wok or skillet, spatula, serving dish',
            ingredients='Assorted vegetables (bell peppers, broccoli, carrots), soy sauce, ginger, rice or noodles',
            thumbnail='https://natashaskitchen.com/wp-content/uploads/2020/08/Vegetable-Stir-Fry-2.jpg',
            likes=1034  # Initial likes count
        )
        
        recipes = [recipe1, recipe2, recipe3, recipe4, recipe5]

        for recipe in recipes:
            try:
                recipe.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {recipe.name}")
# Other parts of the code (User class, initUsers function, etc.) remain unchanged.


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
