import argparse
import logging
import logging.config
import pickle

import numpy as np
import pandas as pd
import sklearn
import yaml
from sklearn import ensemble
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error, mean_absolute_error
from config.flask_config import LOGGING_CONFIG
logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from src.generate_features import choose_features, get_kitty_data
from src.helpers import Timer, fillin_kwargs

methods = dict(gbm=ensemble.GradientBoostingRegressor)

def get_training_data(df, transform = .0000000000001):
    """Grab training data from SQL"""
    
    df = df[df.auction_type == "sale"]
    df.loc[:,["current_price"]] = df.loc[:,["current_price"]].astype(float)*transform # transform the current price variable to a more manageable number
    logger.info("Training data obtained")
    
    return df

def split_data(X, y, random_state = 11, split = 0.9):
    """Split the training data into train/test sets
    
    Args:
        X = training independent variables
        y = training response variable
        random_state = random seed
        split = split percentage (i.e. .9 to training, .1 to testing)

    Returns:
        X_train = training X's
        y_train = training response
        X_test = testing X's
        y_test = testing response
    
    """

    X, y = shuffle(X, y, random_state=random_state)
    offset = int(X.shape[0] * split)
    X_train, y_train = X[:offset], y[:offset]
    X_test, y_test = X[offset:], y[offset:]
    logger.info("Data has been split into testing/training")

    return X_train, y_train, X_test, y_test

def train_model(X_train, y_train, X_test, y_test, method="gbm", save_tmo="models/kitties_model.pkl", params=None):
    """Train a model
    
    Args:
        X_train = training X's
        y_train = training response
        X_test = testing X's
        y_test = testing response
        method = model method - gmb is only model currently available
        save_tmo = file path to save the trained model object
        params = model parameters (set in model config yaml)
    
    Returns:
        tmo = trained model object
    """

    model = methods[method](**params) # define the model

    model.fit(X_train, y_train) # train model
    logger.info("Model has been fit")

    mae = mean_absolute_error(y_test, model.predict(X_test)) # evaluate MAE
    logger.info("MAE: %.4f" % mae)

    if(save_tmo is not None):

        with open(save_tmo, 'wb') as file: # save model
            pickle.dump(model, file)
            logger.info("Model saved to " + save_tmo)

    return model

def run_training(args):
    """Orchestrates the training of the model using command line arguments."""

    with open(args.config, "r") as f:
        config = yaml.load(f)

    kitty_data = get_kitty_data(args.engine_string, kitty_id=None) # grab full kitty_data

    training_data = get_training_data(kitty_data, config["transform_target"]) # pull out data available for training

    X = choose_features(training_data, config["features"])
    y = choose_features(training_data, config["target"])

    X_train, y_train, X_test, y_test = split_data(X, y, random_state = config["random_state"], split = config["split"]) # split data
    
    tmo = train_model(X_train, y_train, X_test, y_test, method = config["method"], save_tmo = config["save_tmo"], params = config["params"]) # train

