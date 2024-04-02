import threading

# import "packages" from flask
from flask import render_template,request, send_from_directory  # import render_template from "public" flask libraries
from flask.cli import AppGroup


# import "packages" from "this" project
from __init__ import app, db, cors  # Definitions initialization


# setup APIs
from api.user import user_api # Blueprint import api definition
from api.video import video_api
from api.stroke import stroke_api
# from api.player import player_api
# database migrations
from api.tips import tips_api
from api.titanic import titanic_api
from api.comments import comments_api

from model.users import initUsers, initVideos
# from model.players import initPlayers
from model.tips import initTips1
from model.tips2 import initTips2
from model.titanic import initTitanic

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition


# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# register URIs
app.register_blueprint(user_api) # register api routes
app.register_blueprint(video_api)
app.register_blueprint(stroke_api)

# app.register_blueprint(player_api)
app.register_blueprint(tips_api)
app.register_blueprint(app_projects) # register app pages
app.register_blueprint(titanic_api) # register app pages
app.register_blueprint(comments_api)

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

@app.route('/videos/<path:path>')
def videos(path):
    return send_from_directory('videos', path)

@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:4100', 'http://127.0.0.1:4100', 'https://nighthawkcoders.github.io']:
        cors._origins = allowed_origin

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    initVideos()
    initUsers()
    initTips1()
    initTips2()
    initTitanic()
    

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)
        
# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    app.run(debug=True, host="0.0.0.0", port="8069")