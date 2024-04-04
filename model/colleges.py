# Import necessary libraries and modules
import os, base64
import json
from __init__ import app, db  # Import the Flask app and SQLAlchemy database instance
from sqlalchemy.exc import IntegrityError  # For handling unique constraint violations

# Define the College class to represent the 'colleges' table in the database
class College(db.Model):
    __tablename__ = 'colleges'  # Specifies the name of the table in the database

    # Define the columns in the 'colleges' table
    _name = db.Column(db.String(255), unique=True, nullable=False, primary_key=True)  # College name column, unique and not nullable
    _link = db.Column(db.String(255), unique=True, nullable=False)  # College link column, unique and not nullable
    _image = db.Column(db.String(255), nullable=True)  # College image column, can be nullable
    
    # Constructor to initialize a College object
    def __init__(self, name, link, img):
        self._name = name    # Initialize the college name
        self._link = link    # Initialize the college link
        self._image = img    # Initialize the college image

    # Getter for college name
    @property
    def name(self):
        return self._name
    
    # Setter for college name
    @name.setter
    def name(self, name):
        self._name = name
    
    # Getter for college link
    @property
    def link(self):
        return self._link
    
    # Setter for college link
    @link.setter
    def link(self, link):
        self._link = link
        
    # Getter for college image
    @property
    def image(self):
        return self._image
    
    # Setter for college image
    @image.setter
    def image(self, img):
        self._image = img
    
    # String representation of the College object in JSON format
    def __str__(self):
        return json.dumps(self.read())
    
    # Method to add a new College object to the database
    def create(self):
        try:
            db.session.add(self)  # Add the College object to the database session
            db.session.commit()  # Commit the transaction to save changes
            return self
        except IntegrityError:  # Handle unique constraint violations
            db.session.remove()  # Remove the session to clear the transaction
            return None

    # Method to read and return College object data as a dictionary
    def read(self):
        return {
            "name": self.name,
            "link": self.link,
            "image": self.image
        }

    # Method to update College object data in the database
    def update(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)  # Update attributes dynamically based on the dictionary keys and values
        db.session.commit()  # Commit the changes to the database
        return self

    # Method to delete a College object from the database
    def delete(self):
        db.session.delete(self)  # Delete the College object from the database session
        db.session.commit()  # Commit the transaction to finalize the deletion

# Function to initialize the College data in the database
def initColleges():
    with app.app_context():
        db.create_all()
        c1 = College(name='Stanford University',link='https://admission.stanford.edu/apply/',img='https://identity.stanford.edu/wp-content/uploads/sites/3/2020/07/block-s-right.png')
        c2 = College(name='Harvard University',link='https://college.harvard.edu/admissions/apply',img='https://1000logos.net/wp-content/uploads/2017/02/Harvard-Logo.png')
        c3 = College(name='MIT',link='https://apply.mitadmissions.org/portal/apply',img='https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/2560px-MIT_logo.svg.png')
        c4 = College(name='Georgia Tech',link='https://admission.gatech.edu/apply/',img='https://brand.gatech.edu/sites/default/files/inline-images/GTVertical_RGB.png')
        c5 = College(name='Duke University',link='https://admissions.duke.edu/apply/',img='https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Duke_Blue_Devils_logo.svg/909px-Duke_Blue_Devils_logo.svg.png')
        c6 = College(name='Yale University',link='https://www.yale.edu/admissions',img='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Yale_University_logo.svg/2560px-Yale_University_logo.svg.png')
        c7 = College(name='Princeton University',link='https://admission.princeton.edu/apply',img='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Princeton_seal.svg/1200px-Princeton_seal.svg.png')
        c8 = College(name='Columbia University',link='https://undergrad.admissions.columbia.edu/apply',img='https://admissions.ucr.edu/sites/default/files/styles/form_preview/public/2020-07/ucr-education-logo-columbia-university.png?itok=-0FD6Ma2')
        c9 = College(name='University of Chicago',link='https://collegeadmissions.uchicago.edu/apply',img='https://upload.wikimedia.org/wikipedia/commons/c/cd/University_of_Chicago_Coat_of_arms.png')
        c10 = College(name='UC Berkeley',link='https://admissions.berkeley.edu/apply-to-berkeley/',img='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Seal_of_University_of_California%2C_Berkeley.svg/1200px-Seal_of_University_of_California%2C_Berkeley.svg.png')
        c11 = College(name='UCLA',link='https://admission.ucla.edu/apply',img='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/UCLA_Bruins_primary_logo.svg/1200px-UCLA_Bruins_primary_logo.svg.png')
        #Add new data to this line
        
        colleges = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11]

        for college in colleges:
            try:
                college.create()  # Add each college to the database
            except IntegrityError:
                db.session.remove()  # Remove the session if there's an integrity error (e.g., duplicate entry)
                print(f"Record exists or error for: {college.name}")
