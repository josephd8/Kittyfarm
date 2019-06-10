import logging
import logging.config
import argparse
import yaml
import os
import subprocess
import re
import boto3
import sqlalchemy
import pandas as pd

from config.flask_config import LOGGING_CONFIG
logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from src.helpers.helpers import fillin_kwargs, create_connection

def get_kitty_data(engine_string, kitty_id=None):
    """Pull kitty data from MySQL into memory

    Args:
        engine_string = MySQL engine connection string
        kitty_id = integer kitty id - if specified it will only grab data for that kitty

    Returns:
        kitty_data = pandas dataframe
    """

    engine = create_connection(engine_string=engine_string)

    if(kitty_id is None): # pull all kitty data if there is no id

        kitty_data = pd.read_sql("select * from kitties", engine)
        logger.info("Kitty data pulled from SQL")

    else: # pull kitty data for one kitty if id is specified

        kitty_data = pd.read_sql("select * from kitties where id = " + str(kitty_id), engine)
        logger.info("Kitty data for kitty # " + str(kitty_id) + " pulled from SQL")

    return kitty_data

def choose_features(df, features_to_use=None):
    """Filter out unwanted features

    Args: 
        df: dataframe of kitty data
        features_to_use: list of features to keep

    Returns:
        X: pandas dataframe containing filtered kitty data

    """

    if features_to_use is not None: # make sure that features_to_use is specified

        X = df[features_to_use]
        logger.info("Features extracted from the kitty data")

    else:
        X = df

    return X

def get_kitty_image(engine_string, kitty_id=None):
    """Pull kitty image from MySQL into memory

    Args:
        engine_string = MySQL engine connection string
        kitty_id = integer kitty id

    Returns:
        kitty_image = url string
    """

    engine = create_connection(engine_string=engine_string)
    kitty_image = pd.read_sql("select image from kitties where id = " + str(kitty_id), engine)
    logger.info("Image for kitty # " + str(kitty_id) + " pulled from SQL")

    return kitty_image["image"][0]

