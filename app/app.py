import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from src.add_kitties import Kitty
from flask_sqlalchemy import SQLAlchemy
import pickle


# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
app.config.from_pyfile('../config/flask_config.py')

# Use pickle to load in the pre-trained model.
with open(app.config["PATH_TO_MODEL"], 'rb') as f:
    model = pickle.load(f)

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("kittyfarm")
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)

@app.route('/')
def index():
    """Main view that allows you to select a kitty to predict

    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        # tracks = db.session.query(Kitty).limit(app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("Index page accessed")
        return render_template('index.html')
    except:
        traceback.print_exc()
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


# @app.route('/add', methods=['POST'])
# def add_entry():
#     """View that process a POST with new song input

#     :return: redirect to index page
#     """

#     try:
#         track1 = Tracks(artist=request.form['artist'], album=request.form['album'], title=request.form['title'])
#         db.session.add(track1)
#         db.session.commit()
#         logger.info("New song added: %s by %s", request.form['title'], request.form['artist'])
#         return redirect(url_for('index'))
#     except:
#         logger.warning("Not able to display tracks, error page returned")
#         return render_template('error.html')

