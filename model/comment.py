from __init__ import db
from sqlalchemy.exc import IntegrityError
import json

# Define the Comment class to manage actions in the 'comments' table
class Comment(db.Model):
    __tablename__ = 'restaurantComments' 

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(255), nullable=False)
    restaurant = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Constructor of a Comment object
    def __init__(self, uid, restaurant, rating):
        self.uid = uid
        self.restaurant = restaurant
        self.rating = rating

    # CRUD create, adds a new record to the Comments table
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Comment object
    def read(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "restaurant": self.restaurant,
            "rating": self.rating
        }

    # CRUD delete: remove self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
def initComments():
    db.create_all()
    comment1 = Comment(
        uid="test1",
        restaurant="test2",
        rating="test1"
    )
    comment2 = Comment(
        uid="test1",
        restaurant="test2",
        rating="test1"
    )
    comment3 = Comment(
        uid="test1",
        restaurant="test2",
        rating="test1"
    )
    comment4 = Comment(
        uid="test1",
        restaurant="test2",
        rating="test1"
    )
    comments=[comment1,comment2,comment3,comment4]
    for comment in comments:
        try:
            comment.create()
        except IntegrityError:
            db.session.remove()
            print("Error")