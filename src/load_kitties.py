import logging
import os
import re
import argparse
import multiprocessing
import glob
import boto3
import yaml
import pandas as pd
import json

import src.helpers.helpers as h
from src.helpers.helpers import create_connection, get_session

logger = logging.getLogger(__name__)

def connect_s3(access_id, access_key):
    
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
    
    obj = s3.Object(bucket,file)
    file_content = obj.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    
    return json_content

def parse_attributes(kitty_json):

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
    hatched = kitty_json["hatched"]
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
    fancy_type, exclusive, cooldown, purrs, watches, hatched, 
    prestige, prestige_ranking, fancy_ranking, body, mouth, eyes,
    pattern, colorprimary, colorsecondary, colortertiary, coloreyes,
    mother_id, mother_fancy, mother_exclusive, father_id,
    father_fancy, father_exclusive, start_price, end_price,
    current_price, auction_type, auction_start, auction_end,
    auction_duration]

def kitties_to_sql(kitties_json, engine_string):
    
    kitty_list = [parse_attributes(kitty) for kitty in kitties_json["kitties"]]
    
    kitties_df = pd.DataFrame(kitty_list)
    kitties_df.drop(0, axis=1)
    
    column_names = ["id", "name", "image", "generation", "birthday", "color", "fancy",
    "fancy_type", "exclusive", "cooldown", "purrs", "watches", "hatched", 
    "prestige", "prestige_ranking", "fancy_ranking", "body", "mouth", "eyes",
    "pattern", "colorprimary", "colorsecondary", "colortertiary", "coloreyes",
    "mother_id", "mother_fancy", "mother_exclusive", "father_id",
    "father_fancy", "father_exclusive", "start_price", "end_price",
    "current_price", "auction_type", "auction_start", "auction_end",
    "auction_duration"]
    
    kitties_df.columns = column_names
    
    engine = create_connection(engine_string=engine_string)
    
    kitties_df.to_sql("kitties", engine, if_exists="append", index = False)
    
    return True

def land_kitties(args):

    print(args.engine_string)
    print(args.bucket)
    print(args.access_id)
    print(args.access_key)

    s3 = connect_s3(args.access_id, args.access_key)

    files = get_s3_file_names(s3, "s3://jdc-nu")

    cntr = 0
    for file in files:

        kitties_json = load_kitty_json(file, s3, args.bucket)
        kitties_to_sql(kitties_json, args.engine_string)

        cntr = cntr + len(kitties_json["kitties"])
        print(cntr)

    return

def get_file_names(top_dir):
    """Get all file names in a directory subtree

    Args:
        top_dir (str): The base directory from which to get list_of_files from

    Returns: List of file locations

    """

    if top_dir.startswith("s3://"):
        list_of_files = get_s3_file_names(top_dir)
    else:
        top_dir = top_dir[:-1] if top_dir[-1] == "/" else top_dir
        list_of_files = glob.glob(top_dir+'/*.csv', recursive=True)

    return list_of_files


def load_csv(path, **kwargs):
    """Wrapper function for `pandas.read_csv()` method to enable multiprocessing.

    """
    return pd.read_csv(path, **kwargs)


def load_column_as_list(path, column=0, **kwargs):

    for k in kwargs:
        logger.debug(kwargs[k])

    df = pd.read_csv(path, **kwargs)

    return df[column].tolist()


def load_csvs(file_names=None, directory=None, n_cores=1):
    """Loads multiple CSVs into a single Pandas dataframe.

    Given either a directory name (which can be local or an s3 bucket prefix) or a list of CSV files, this function
    will load all CSVs into a single Pandas DataFrame. It assumes the same schema exists across all CSVs.
    
    Args:
        file_names (list of str, default=None): List of files to load. If None, `directory` should be given. 
        directory (str, default=None): Directory containing files to be loaded. If None, `filenames` should be given.
        n_cores (int, default=1): Number of processes (i.e. CPUs) to load csvs on.
            If -1 given, number of available CPUs will be used. 

    Returns: Single dataframe with data from all files loaded

    """

    # Get list of files
    if file_names is None and directory is None:
        raise ValueError("filenames or directory must be given")
    elif file_names is None:
        file_names = get_file_names(directory)

    if n_cores == -1:
        n_cores = multiprocessing.cpu_count()

    logger.info("Utilizing {} cores".format(str(n_cores)))

    with h.Timer("Reading CSVs", logger):
        pool = multiprocessing.Pool(processes=n_cores)

        df_list = pool.map(load_csv, file_names)

        # Concatenate list of dataframes into one dataframe
        df = pd.concat(df_list, ignore_index=True)

    return df


def load_data(config):
    how = config["how"].lower()

    if how == "load_csv":
        if "load_csv" not in config:
            raise ValueError("'how' given as 'load_csv' but 'load_csv' not in configuration")
        else:
            df = load_csv(**config["load_csv"])
    elif how == "load_csvs":
        if config["load_csvs"] is None:
            raise ValueError("'how' given as 'load_csvs' but 'load_csvs' not in configuration")
        else:
            df = load_csvs(**config["load_csvs"])
    else:
        raise ValueError("Options for 'how' are 'load_csv' and 'load_csvs' but %s was given" % how)

    return df


def run_loading(args):
    """Loads config and executes load data set

    Args:
        args: From argparse, should contain args.config and optionally, args.save
            args.config (str): Path to yaml file with load_data as a top level key containing relevant configurations
            args.save (str): Optional. If given, resulting dataframe will be saved to this location.

    Returns: None

    """
    with open(args.config, "r") as f:
        config = yaml.load(f)

    df = load_data(**config["load_data"])

    if args.save is not None:
        df.to_csv(args.save)
