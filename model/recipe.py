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
    _description = db.Column(db.String(255), nullable=False)
    _recipe_image = db.Column(db.String(255), nullable=False)
    _recipe = db.Column(db.String(255), nullable=False)
    _ingredients = db.Column(db.String(255), nullable=False)
    _user_id = db.Column(db.String(255), nullable=False)
    _category = db.Column(db.String(255), nullable=False)

    def __init__(self, name, description, recipe_image, recipe, ingredients, user_id, category=""):
        self._name = name
        self._description = description
        self._recipe_image = recipe_image
        self._recipe = recipe
        self._ingredients = ingredients
        self._user_id = user_id
        self._category = category

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        self.description = description
    
    @property
    def recipe_image(self):
        return self._recipe_image
    
    @recipe_image.setter
    def recipe_image(self, recipe_image):
        self._recipe_image = recipe_image

    @property
    def recipe(self):
        return self._recipe
    
    @recipe.setter
    def recipe(self, recipe):
        self._recipe = recipe

    @property
    def ingredients(self):
        return self._ingredients
    
    @ingredients.setter
    def ingredients(self, ingredients):
        self._ingredients = ingredients

    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, category):
        self._category = category

    def create(self, base64_encoded):
        try:
            path = app.config['UPLOAD_FOLDER']
            file_decode = base64.b64decode(base64_encoded)
            db.session.add(self)
            db.session.commit()

            self._recipe_image = str(self.id) + str(self._recipe_image)
            output_file_path = os.path.join(path, str(self._recipe_image))
            with open(output_file_path, 'wb') as output_file:
                output_file.write(file_decode)

            db.session.commit()

            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        try:
            path = app.config['UPLOAD_FOLDER']
            file = os.path.join(path, self._recipe_image)
            file_text = open(file, 'rb')
            file_read = file_text.read()
            file_encode = base64.encodebytes(file_read)
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "recipe_image": self._recipe_image,
                "base64": str(file_encode),
                "recipe": self.recipe,
                "ingredients": self.ingredients,
                "user_id": self.user_id,
                "category": self.category
            }
        except:
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "recipe_image": "",
                "base64": "",
                "recipe": self.recipe,
                "ingredients": self.ingredients,
                "user_id": self.user_id,
                "category": self.category
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
            description="blah blah blah", 
            recipe_image="pizza.png", 
            recipe=0, 
            ingredients="Cheese blah afdsj", 
            user_id="aiden",
            category="Italian"
        )

        recipes = [recipe1]

        """Builds sample user/note(s) data"""
        for recipe in recipes:
            try:
                path = app.config['UPLOAD_FOLDER']
                file = os.path.join(path, recipe.recipe_image)
                file_text = open(file, 'rb')
                file_read = file_text.read()
                file_encode = base64.encodebytes(file_read)
                recipe.create(file_encode)
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {recipe.recipe_image}")

# Other parts of the code (User class, initUsers function, etc.) remain unchanged.


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _email = db.Column(db.String(255), unique=True, nullable=False)
    _dob = db.Column(db.Date)
    _role = db.Column(db.String(20), default="User", nullable=False)
    # Define _preferences as an ARRAY of strings
    _preferences = db.Column(db.String(255), nullable=False)


    # Demo purposes
    #

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    # posts = db.relationship("Post", cascade="all, delete", backref="users", lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, email, password="123qwerty", dob=date.today(), role="User", preferences="none"):
        self._name = name  # variables with self prefix become part of the object,
        self._uid = uid
        self.set_password(password)
        self._email = email
        self._dob = dob
        self._role = role
        self._preferences = preferences
        
    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name

    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email
    

    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid

    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid

    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid

    @property
    def password(self):
        return (
            self._password[0:10] + "..."
        )  # because of security only show 1st characters

    # update password, this is conventional setter
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(
            password, "pbkdf2:sha256", salt_length=10
        )

    # check password parameter versus stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result

    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def dob(self):
        dob_string = self._dob.strftime("%m-%d-%Y")
        return dob_string

    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob


    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role):
        self._role = role

    def is_admin(self):
        return self._role == "Admin"
    
    # ... (existing code)

    @property
    def preferences(self):
        return self._preferences
    
    @preferences.setter
    def set_preferences(self, preferences):
        self._preferences = preferences
    
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "dob": self.dob,
            # "age": self.age,
            "role": self.role,
            "email": self.email,
            "preferences": self.preferences
            # "post s": [post.read() for post in self.posts]
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", password=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        db.session.commit()
        return self
    
    def update_email(self, email=""):
        if len(email) >= 5 and "@" in email:
            self.email = email
        db.session.commit()
        print(self.email)
        return self
    
    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = User(
            name="Aiden Kim", 
            uid="aiden", 
            email="aidenhw.kim@gmail.com",
            password="password",
            dob=date(2001, 9, 12),
            role="Admin"
        )
        u2 = User(
            name="Thomas Edison", 
            uid="toby", 
            email = "toby@gmail.com",
            password="123toby",
            dob=date(1945, 8, 6)
        )
        u3 = User(
            name="Jeff",
            uid="jeff",
            password='123jeff',
            email = "jeff@gmail.com",
            dob=date(2020, 12, 25)
        )
        users = [u1, u2, u3]
        # print("-------------------------- USERS -----------------------------")
        # print(users)
        """Builds sample user/note(s) data"""
        # i = 0
        for user in users:
            try:
                # print(i)
                # print(user)
                user.create()
            except IntegrityError:
                """fails with bad or duplicate data"""
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")