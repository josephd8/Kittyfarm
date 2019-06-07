import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
import flask
from src.add_kitties import Kitty
from flask_sqlalchemy import SQLAlchemy
import pickle
import yaml
import sklearn
import numpy as np
import matplotlib.pyplot as plt
from sklearn import ensemble
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error, mean_absolute_error

from src.generate_features import get_kitty_data, choose_features, get_kitty_image

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
app.config.from_pyfile('../config/flask_config.py')

with open(app.config["MODEL_CONFIG"], "r") as f:
    model_config = yaml.load(f)

# Use pickle to load in the pre-trained model.
with open(app.config["PATH_TO_MODEL"], 'rb') as f:
    model = pickle.load(f)

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(__name__)
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)

@app.route('/', methods = ["GET", "POST"])
def index():
    """Main view that allows you to select a kitty to predict

    Create view into index page that allows a user to input a kitty id and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    if flask.request.method == 'GET':
        logger.info("Index rendered.")
        return(flask.render_template('index.html'))

    if flask.request.method == 'POST':
        
        try:
            kitty_id = flask.request.form['kitty_id']
            logger.info("Kitty id is " + str(kitty_id))
            data = get_kitty_data(app.config["HOME_ENGINE_STRING"], kitty_id)        
            X = choose_features(data, model_config["features"])
            logger.info("Prediction data shape is " + str(X.shape))
            prediction = model.predict(X)[0]
            logger.info("Prediction is " + str(prediction))
            kitty_image = get_kitty_image(app.config["HOME_ENGINE_STRING"], kitty_id)
            return flask.render_template('index.html',
                                     result=prediction,
                                     image=kitty_image)
        except:
            traceback.print_exc()
            logger.warning("kitty ID not valid")
            return render_template('error.html')


