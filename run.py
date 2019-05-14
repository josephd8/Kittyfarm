"""Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

Current commands enabled:

To create a database for Tracks with an initial song:

    `python run.py create --artist="Britney Spears" --title="Radar" --album="Circus"`

To add a song to an already created database:

    `python run.py ingest --artist="Britney Spears" --title="Radar" --album="Circus"`
"""
import datetime
import argparse
import logging.config
logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("run-penny-lane")

from src.add_kitties import create_db, add_kitty


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run components of the model source code")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create", description="Create database")

    sb_create.add_argument("--id", default=0, help="id of kitty")
    sb_create.add_argument("--name", default="OG", help="name of kitty")
    sb_create.add_argument("--generation", default=0, help="generation of kitty")
    sb_create.add_argument("--birthday", default=datetime.datetime.utcnow, help="birthdate of kitty")
    sb_create.add_argument("--color", default="gold", help="main color of kitty")
    sb_create.add_argument("--fancy", default=True, help="fancy status of kitty")
    sb_create.add_argument("--exclusive", default=True, help="exclusive status of kitty")
    sb_create.add_argument("--fancy_type", default="TheFanciest", help="fancy type of kitty")
    sb_create.add_argument("--cooldown", default=11, help="cooldown index of kitty")
    sb_create.add_argument("--purrs", default=7, help="# of purrs for kitty")
    sb_create.add_argument("--watches", default=3, help="# of watches for kitty")
    sb_create.add_argument("--hatched", default=False, help="hatch status of kitty")
    sb_create.add_argument("--prestige", default=True, help="prestige status of kitty")
    sb_create.add_argument("--prestige_type", default="ThePrestigiest", help="prestige type of kitty")
    sb_create.add_argument("--prestige_ranking", default=1, help="prestige ranking of kitty")
    sb_create.add_argument("--fancy_ranking", default=1, help="fancy ranking of kitty")
    sb_create.add_argument("--body", default="body", help="body of kitty")
    sb_create.add_argument("--mouth", default="mouth", help="mouth of kitty")
    sb_create.add_argument("--eyes", default="eyes", help="eyes of kitty")
    sb_create.add_argument("--pattern", default="pattern", help="pattern of kitty")
    sb_create.add_argument("--colorprimary", default="blue", help="primary color of kitty")
    sb_create.add_argument("--colorsecondary", default="green", help="secondary color of kitty")
    sb_create.add_argument("--colortertiary", default="purple", help="tertiary color of kitty")
    sb_create.add_argument("--coloreyes", default="gold", help="eye color of kitty")
    sb_create.add_argument("--mother_id", default=None, help="mother's id of kitty")
    sb_create.add_argument("--mother_fancy", default=None, help="mother's fancy status of kitty")
    sb_create.add_argument("--mother_exclusive", default=None, help="mother's exclusive status of kitty")
    sb_create.add_argument("--father_id", default=None, help="father's id of kitty")
    sb_create.add_argument("--father_fancy", default=None, help="father's fancy status of kitty")
    sb_create.add_argument("--father_exclusive", default=None, help="father's exclusive status of kitty")
    sb_create.add_argument("--start_price", default=10000000, help="start price for kitty on auction")
    sb_create.add_argument("--end_price", default=10000000, help="end price for kitty on auction")
    sb_create.add_argument("--current_price", default=10000000, help="current price for kitty on auction")
    sb_create.add_argument("--auction_start", default=datetime.datetime.utcnow, help="auction start for kitty")
    sb_create.add_argument("--auction_end", default=datetime.datetime.utcnow, help="auction end for kitty")
    sb_create.add_argument("--auction_duration", default=1111111, help="auction duration for kitty")
    sb_create.add_argument("--auction_type", default="sale", help="auction type (sale or sire) for kitty")

    sb_create.set_defaults(func=create_db)

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")

    sb_ingest.add_argument("--id", default=0, help="id of kitty")
    sb_ingest.add_argument("--name", default="OG", help="name of kitty")
    sb_ingest.add_argument("--generation", default=0, help="generation of kitty")
    sb_ingest.add_argument("--birthday", default=datetime.datetime.utcnow, help="birthdate of kitty")
    sb_ingest.add_argument("--color", default="gold", help="main color of kitty")
    sb_ingest.add_argument("--fancy", default=True, help="fancy status of kitty")
    sb_ingest.add_argument("--exclusive", default=True, help="exclusive status of kitty")
    sb_ingest.add_argument("--fancy_type", default="TheFanciest", help="fancy type of kitty")
    sb_ingest.add_argument("--cooldown", default=11, help="cooldown index of kitty")
    sb_ingest.add_argument("--purrs", default=7, help="# of purrs for kitty")
    sb_ingest.add_argument("--watches", default=3, help="# of watches for kitty")
    sb_ingest.add_argument("--hatched", default=False, help="hatch status of kitty")
    sb_ingest.add_argument("--prestige", default=True, help="prestige status of kitty")
    sb_ingest.add_argument("--prestige_type", default="ThePrestigiest", help="prestige type of kitty")
    sb_ingest.add_argument("--prestige_ranking", default=1, help="prestige ranking of kitty")
    sb_ingest.add_argument("--fancy_ranking", default=1, help="fancy ranking of kitty")
    sb_ingest.add_argument("--body", default="body", help="body of kitty")
    sb_ingest.add_argument("--mouth", default="mouth", help="mouth of kitty")
    sb_ingest.add_argument("--eyes", default="eyes", help="eyes of kitty")
    sb_ingest.add_argument("--pattern", default="pattern", help="pattern of kitty")
    sb_ingest.add_argument("--colorprimary", default="blue", help="primary color of kitty")
    sb_ingest.add_argument("--colorsecondary", default="green", help="secondary color of kitty")
    sb_ingest.add_argument("--colortertiary", default="purple", help="tertiary color of kitty")
    sb_ingest.add_argument("--coloreyes", default="gold", help="eye color of kitty")
    sb_ingest.add_argument("--mother_id", default=None, help="mother's id of kitty")
    sb_ingest.add_argument("--mother_fancy", default=None, help="mother's fancy status of kitty")
    sb_ingest.add_argument("--mother_exclusive", default=None, help="mother's exclusive status of kitty")
    sb_ingest.add_argument("--father_id", default=None, help="father's id of kitty")
    sb_ingest.add_argument("--father_fancy", default=None, help="father's fancy status of kitty")
    sb_ingest.add_argument("--father_exclusive", default=None, help="father's exclusive status of kitty")
    sb_ingest.add_argument("--start_price", default=10000000, help="start price for kitty on auction")
    sb_ingest.add_argument("--end_price", default=10000000, help="end price for kitty on auction")
    sb_ingest.add_argument("--current_price", default=10000000, help="current price for kitty on auction")
    sb_ingest.add_argument("--auction_start", default=datetime.datetime.utcnow, help="auction start for kitty")
    sb_ingest.add_argument("--auction_end", default=datetime.datetime.utcnow, help="auction end for kitty")
    sb_ingest.add_argument("--auction_duration", default=1111111, help="auction duration for kitty")
    sb_ingest.add_argument("--auction_type", default="sale", help="auction type (sale or sire) for kitty")

    sb_ingest.set_defaults(func=add_kitty)

    args = parser.parse_args()
    args.func(args)
