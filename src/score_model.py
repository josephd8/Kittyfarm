import logging
import logging.config
import argparse
import yaml
import os
import subprocess
import re
import datetime
import pickle
import sklearn
import pandas as pd
import numpy as np

from config.flask_config import LOGGING_CONFIG
logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from src.helpers import Timer, fillin_kwargs
from src.generate_features import choose_features, get_kitty_data
from sklearn.linear_model import LogisticRegression, LinearRegression

def score_model(engine_string, kitty_id, path_to_tmo, features):
    """Predict a kitty's price

    Args:
        engine_string = SQL connection engine string
        kitty_id = integer id of kitty to score
        path_to_tmo = string path to the trained model object
        features = list of features to keep for prediction

    Returns:
        prediction: predicted kitty price

    """

    df = get_kitty_data(engine_string, kitty_id)
    logger.info("Kitty data loaded.")
    
    with open(path_to_tmo, "rb") as f: # load the model object
        model = pickle.load(f)
    logger.info("Model loaded.")

    X = choose_features(df, features) # filter out unnecessary features

    y_predicted = model.predict(X) # make prediction
    logger.info("Finished predicting")

    return y_predicted


def run_scoring(args):
    """Run scoring"""

    with open(args.config, "r") as f:
        config = yaml.load(f)
    logger.info("Scoring config is loaded")

    y_predicted = score_model(args.engine_string, args.kitty_id, config["path_to_tmo"], config["features"])[0]
    logger.info("Prediction: " + str(y_predicted))

    return
