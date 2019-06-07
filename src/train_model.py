import argparse
import logging
import pickle

import numpy as np
import pandas as pd
import sklearn
import yaml
import matplotlib.pyplot as plt
from sklearn import ensemble
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error, mean_absolute_error

from src.generate_features import choose_features, get_kitty_data
from src.helpers import Timer, fillin_kwargs

logger = logging.getLogger(__name__)

methods = dict(gbm=ensemble.GradientBoostingRegressor)

def get_training_data(df, transform = .0000000000001):
    
    df = df[df.auction_type == "sale"]
    df.loc[:,["current_price"]] = df.loc[:,["current_price"]]*transform
    
    return df

def split_data(X, y, random_state = 11, split = 0.9):

    X, y = shuffle(X, y, random_state=random_state)
    offset = int(X.shape[0] * split)
    X_train, y_train = X[:offset], y[:offset]
    X_test, y_test = X[offset:], y[offset:]

    return X_train, y_train, X_test, y_test

def train_model(X_train, y_train, X_test, y_test, method="gbm", save_tmo="models/kitties_model.pkl", params=None):

    model = methods[method](**params)

    model.fit(X_train, y_train)

    mae = mean_absolute_error(y_test, model.predict(X_test))
    print("MSE: %.4f" % mae)

    if(save_tmo is not None):

        with open(save_tmo, 'wb') as file:
            pickle.dump(model, file)

    return model



# def train_model(df, method="gbm", save_tmo=None, add_evalset=True, **kwargs):

#     assert method in methods.keys()  # `methods` defined at top of file, possible methods for training

#     # If "get_target" in the config file under "train_model", will get the target data for supervised learning
#     # Otherwise y = None and the model must be unsupervised.
#     if "get_target" in kwargs:
#         y = get_target(df, **kwargs["get_target"])
#         df = df.drop(labels=[kwargs["get_target"]["target"]], axis=1)
#     else:
#         y = None

#     # If "choose_features" in the config file under "train_model", will reduce the feature set to those listed
#     if "choose_features" in kwargs:
#         X = choose_features(df, **kwargs["choose_features"])
#     else:
#         X = df

#     # If "fit", "predict", and other configuration options listed at the top of the file under
#     # "train_model_kwargs" are not in the "train_data" configurations, creates empty dictionaries
#     # in their place to allow consistent calling of the functions below
#     kwargs = fillin_kwargs(train_model_kwargs, kwargs)

#     # Splits the training data according to the "split_data" parameters. If this is an empty dictionary
#     # (from prior step, because it is not in the configuration file), then the full dataset is returned (train_size=1)
#     X, y = split_data(X, y, **kwargs["split_data"])

#     # Instantiates a model class for the training `method` provided
#     model = methods[method](**kwargs["params"])

#     # If `add_evalset` is given as true and validation sets are created in the data split, will add the validation
#     # sets to the model fit parameters for use by the model in training for validation (e.g. for xgboost)
#     if "validate" in X and "validate" in y and add_evalset:
#         kwargs["fit"]["eval_set"] = [(X["validate"], y["validate"])]

#     # Fit the model with the training data and time doing so
#     with Timer("model training", logger) as t:
#         model.fit(X["train"], y["train"], **kwargs["fit"])

#     # Save the trained model object
#     if save_tmo is not None:
#         with open(save_tmo, "wb") as f:
#             pickle.dump(model, f)
#         logger.info("Trained model object saved to %s", save_tmo)

#     return model


def run_training(args):
    """Orchestrates the training of the model using command line arguments."""

    with open(args.config, "r") as f:
        config = yaml.load(f)

    kitty_data = get_kitty_data(args.engine_string, kitty_id=None)

    training_data = get_training_data(kitty_data, config["transform_target"])

    X = choose_features(training_data, config["features"])
    y = choose_features(training_data, config["target"])

    print(X.columns)
    print(X.shape)
    X_train, y_train, X_test, y_test = split_data(X, y, random_state = config["random_state"], split = config["split"])
    
    print(X_train.shape)
    print(y_train.shape)
    print(X_test.shape)
    print(y_test.shape)
    tmo = train_model(X_train, y_train, X_test, y_test, method = config["method"], save_tmo = config["save_tmo"], params = config["params"])


    # logger.info("Training configuration file, %s, loaded", args.config)

    # if args.input is not None:
    #     df = pd.read_csv(args.input)
    #     logger.info("Features for input into model loaded from %s", args.input)
    # elif "generate_features" in config and "save_features" in config["generate_features"]:
    #     df = pd.read_csv(config["generate_features"]["save_features"])
    #     logger.info("Features for input into model loaded from %s", config["generate_features"]["save_features"])
    # else:
    #     raise ValueError("Path to CSV for input data must be provided through --input or "
    #                      "'load_data' configuration must exist in config file")

    # tmo = train_model(df, **config["train_model"])

    

    # if args.output is not None:
    #     with open(args.output, "wb") as f:
    #         pickle.dump(tmo, f)
    #     logger.info("Trained model object saved to %s", args.output)
