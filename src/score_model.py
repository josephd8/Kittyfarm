import logging
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

from src.helpers import Timer, fillin_kwargs
from src.generate_features import choose_features, get_kitty_data
from sklearn.linear_model import LogisticRegression, LinearRegression

logger = logging.getLogger(__name__)

score_model_kwargs = ["predict"]


def score_model(engine_string, kitty_id, path_to_tmo, features):

    df = get_kitty_data(engine_string, kitty_id)
    
    with open(path_to_tmo, "rb") as f:
        model = pickle.load(f)

    X = choose_features(df, features)

    y_predicted = model.predict(X)

    return y_predicted


def run_scoring(args):
    with open(args.config, "r") as f:
        config = yaml.load(f)

    # if args.input is not None:
    #     df = pd.read_csv(args.input)
    # elif "generate_features" in config and "save_features" in config["generate_features"]:
    #     df = pd.read_csv(config["generate_features"]["save_features"])
    # else:
    #     raise ValueError("Path to CSV for input data must be provided through --input or "
    #                      "'load_data' configuration must exist in config file")

    y_predicted = score_model(args.engine_string, args.kitty_id, config["path_to_tmo"], config["features"])
    print(y_predicted)