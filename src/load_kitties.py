import logging
import logging.config
import os
import re
import argparse
import multiprocessing
import glob
import boto3
import yaml
import pandas as pd
import json

from config.flask_config import LOGGING_CONFIG
logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

import src.helpers.helpers as h
from src.helpers.helpers import create_connection, get_session

def connect_s3(access_id, access_key):
    """Make connection to s3"""
    
    s3 = boto3.resource('s3',
                    aws_access_key_id=access_id,
                    aws_secret_access_key=access_key)
    
    return s3

def get_s3_file_names(s3, s3_bucket_path):
    """Get all file names in an s3 bucket 

    Args:
        s3_bucket_path (str): S3 path to bucket containing all files to list (Ex: `s3://jdc-nu`)

    Returns: List of all S3 file locations

    """

    # parse s3 path for bucket name and prefix
    regex = r"s3://([\w._-]+)"
    m = re.match(regex, s3_bucket_path)
    s3bucket_name = m.group(1) 

    # Get s3 bucket handle
    s3bucket = s3.Bucket(s3bucket_name)

    # Get all file names in the `s3bucket`
    files = []
    for object in s3bucket.objects.all():
        file = object.key
        files.append(file)

    return files

def load_kitty_json(file, s3, bucket = "jdc-nu"):
    """Load kitty json file from s3 to json"""
    
    obj = s3.Object(bucket,file) # connect to file
    file_content = obj.get()['Body'].read().decode('utf-8') # read content
    json_content = json.loads(file_content) # json format

    return json_content

def parse_attributes(kitty_json):

    # grabbing attibutes for the kitty out of the json
    id = kitty_json["id"]
    name = kitty_json["name"]
    image = kitty_json["image_url_png"]
    generation = kitty_json["generation"]
    birthday = kitty_json["created_at"]
    color = kitty_json["color"]
    fancy = kitty_json["is_fancy"]
    fancy_type = kitty_json["fancy_type"]
    exclusive = kitty_json["is_exclusive"]
    cooldown = kitty_json["status"]["cooldown_index"]
    purrs = kitty_json["purrs"]["count"]
    watches = kitty_json["watchlist"]["count"]

    prestige = kitty_json["is_prestige"]
    prestige_type = kitty_json["prestige_type"]
    prestige_ranking = kitty_json["prestige_ranking"]
    fancy_ranking = kitty_json["fancy_ranking"]

    if(len(kitty_json["enhanced_cattributes"]) == 0):

        body = None
        coloreyes = None
        eyes = None
        pattern = None
        mouth = None
        colorprimary = None
        colorsecondary = None
        colortertiary = None

    else:

        body = kitty_json["enhanced_cattributes"][0]["description"] #body
        coloreyes = kitty_json["enhanced_cattributes"][1]["description"] #coloreyes
        eyes = kitty_json["enhanced_cattributes"][2]["description"] #eyes
        pattern = kitty_json["enhanced_cattributes"][3]["description"] #pattern
        mouth = kitty_json["enhanced_cattributes"][4]["description"] #mouth
        colorprimary = kitty_json["enhanced_cattributes"][5]["description"] #colorprimary
        colorsecondary = kitty_json["enhanced_cattributes"][6]["description"] #colorsecondary
        colortertiary = kitty_json["enhanced_cattributes"][7]["description"] #colortertiary
    
    if(len(kitty_json["matron"]) == 0):
        
        mother_id = None
        mother_fancy = None
        mother_exclusive = None
        
    else:

        mother_id = kitty_json["matron"]["id"]
        mother_fancy = kitty_json["matron"]["is_fancy"]
        mother_exclusive = kitty_json["matron"]["is_exclusive"]
    
    
    if(len(kitty_json["sire"]) == 0):
        
        father_id = None
        father_fancy = None
        father_exclusive = None
        
    else:
        
        father_id = kitty_json["sire"]["id"]
        father_fancy = kitty_json["sire"]["is_fancy"]
        father_exclusive = kitty_json["sire"]["is_exclusive"]
    
    
    if(len(kitty_json["auction"]) == 0):
        
        start_price = None
        end_price = None
        current_price = None
        auction_type = None
        auction_start = None
        auction_end = None
        auction_duration = None
        
    else:
        
        start_price = kitty_json["auction"]["start_price"]
        end_price = kitty_json["auction"]["end_price"]
        current_price = kitty_json["auction"]["current_price"]
        auction_type = kitty_json["auction"]["type"]
        auction_start = kitty_json["auction"]["start_time"]
        auction_end = kitty_json["auction"]["end_time"]
        auction_duration = kitty_json["auction"]["duration"]
    
    return [id, name, image, generation, birthday, color, fancy,
    fancy_type, exclusive, cooldown, purrs, watches,
    prestige, prestige_ranking, fancy_ranking, body, mouth, eyes,
    pattern, colorprimary, colorsecondary, colortertiary, coloreyes,
    mother_id, mother_fancy, mother_exclusive, father_id,
    father_fancy, father_exclusive, start_price, end_price,
    current_price, auction_type, auction_start, auction_end,
    auction_duration]

def kitties_to_sql(kitties_json, engine_string):
    """Take a json of kitties and ingest into SQL
    
    Args:
        kitties_json = json containing a "kitties" object
        engine_string = SQL connection engine string

    Returns:
        None
    
    """
    
    kitty_list = [parse_attributes(kitty) for kitty in kitties_json["kitties"]] # parse attributes for each kitty
    
    kitties_df = pd.DataFrame(kitty_list)
    kitties_df.drop(0, axis=1) # format dataframe
    
    column_names = ["id", "name", "image", "generation", "birthday", "color", "fancy",
    "fancy_type", "exclusive", "cooldown", "purrs", "watches",
    "prestige", "prestige_ranking", "fancy_ranking", "body", "mouth", "eyes",
    "pattern", "colorprimary", "colorsecondary", "colortertiary", "coloreyes",
    "mother_id", "mother_fancy", "mother_exclusive", "father_id",
    "father_fancy", "father_exclusive", "start_price", "end_price",
    "current_price", "auction_type", "auction_start", "auction_end",
    "auction_duration"]
    
    kitties_df.columns = column_names # update column names
    
    engine = create_connection(engine_string=engine_string)
    
    kitties_df.to_sql("kitties", engine, if_exists="append", index = False) # ingest to sql
    
    return True

def land_kitties(args):
    """Land kitties from the cloud to the ground (s3 to SQL)

    Args: argparse args

    Returns: None
    
    """

    s3 = connect_s3(args.access_id, args.access_key) # make s3 connection
    logger.info("Connected to s3")

    files = get_s3_file_names(s3, "s3://jdc-nu") # get filenames
    logger.info("Extracted filenames from s3 bucket")

    cntr = 0
    logger.info("Parsing kitties to SQL")
    for file in files:

        kitties_json = load_kitty_json(file, s3, args.bucket) # load json
        kitties_to_sql(kitties_json, args.engine_string) # parse and send to sql

        cntr = cntr + len(kitties_json["kitties"])
        logger.info(str(cntr) + " kitties have landed")

    logger.info("KITTIES HAVE LANDED.")
    return