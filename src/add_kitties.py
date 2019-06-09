
import argparse
import logging.config
import yaml
import os
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, DateTime, Boolean, Float
from sqlalchemy.orm import sessionmaker

from src.helpers.helpers import create_connection, get_session


logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()

class Kitty(Base):
    """Create a data model for the database to be set up for to store kitties

    """

    __tablename__ = "kitties"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=False, nullable=True)
    image = Column(String(200), unique=True, nullable=False)
    generation = Column(Integer, unique=False, nullable=True)
    birthday = Column(DateTime, unique=False, nullable=True)
    color = Column(String(100), unique=False, nullable=True)
    fancy = Column(Boolean, unique=False, nullable=True)
    fancy_type = Column(String(100), unique=False, nullable=True)
    exclusive = Column(Boolean, unique=False, nullable=True)
    cooldown = Column(Integer, unique=False, nullable=True)
    purrs = Column(Integer, unique=False, nullable=True)
    watches = Column(Integer, unique=False, nullable=True)
    # hatched = Column(Boolean, unique=False, nullable=True)
    prestige = Column(Boolean, unique=False, nullable=True)
    prestige_type = Column(String(100), unique=False, nullable=True)
    prestige_ranking = Column(Integer, unique=False, nullable=True)
    fancy_ranking = Column(Integer, unique=False, nullable=True)
    body = Column(String(100), unique=False, nullable=True)
    mouth = Column(String(100), unique=False, nullable=True)
    eyes = Column(String(100), unique=False, nullable=True)
    pattern = Column(String(100), unique=False, nullable=True)
    colorprimary = Column(String(100), unique=False, nullable=True)
    colorsecondary = Column(String(100), unique=False, nullable=True)
    colortertiary = Column(String(100), unique=False, nullable=True)
    coloreyes = Column(String(100), unique=False, nullable=True)
    mother_id = Column(Integer, unique=False, nullable=True)
    mother_fancy = Column(Boolean, unique=False, nullable=True)
    mother_exclusive = Column(Boolean, unique=False, nullable=True)
    father_id = Column(Integer, unique=False, nullable=True)
    father_fancy = Column(Boolean, unique=False, nullable=True)
    father_exclusive = Column(Boolean, unique=False, nullable=True)
    start_price = Column(Float, unique=False, nullable=True)
    end_price = Column(Float, unique=False, nullable=True)
    current_price = Column(Float, unique=False, nullable=True)
    auction_type = Column(String(100), unique=False, nullable=True)
    auction_start = Column(DateTime, unique=False, nullable=True)
    auction_end = Column(DateTime, unique=False, nullable=True)
    auction_duration = Column(Float, unique=False, nullable=True)    

    def __repr__(self):
        return '<Kitty(id: %s, name: %s)>' % (self.id, self.name)


def create_db(args):
    """Creates a database with the data model given by obj:`apps.models.Track`

    """

    engine = create_connection(engine_string=args.engine_string)
    
    if(engine.has_table("kitties")):
        Base.metadata.drop_all(bind=engine, tables=[Kitty.__table__])

    Base.metadata.create_all(engine)

    session = get_session(engine=engine)

    logger.info("Database created for kitties")
    session.close()


def add_kitty(args):
    """Seeds an existing database with additional kitty.

    Args:
        args: Argparse args - should include ...

    Returns:None

    """

    session = get_session(engine_string=args.engine_string)

    kitty = Kitty(
        id = args.id, 
        name = args.name,
        image = args.image,
        generation = args.generation,
        birthday = args.birthday,
        color = args.color,
        fancy = args.fancy,
        fancy_type = args.fancy_type,
        exclusive = args.exclusive,
        cooldown = args.cooldown,
        purrs = args.purrs,
        watches = args.watches,
        # hatched = args.hatched,
        prestige = args.prestige,
        prestige_type = args.prestige_type,
        prestige_ranking = args.prestige_ranking,
        fancy_ranking = args.fancy_ranking,
        body = args.body,
        mouth = args.mouth,
        eyes = args.eyes,
        pattern = args.pattern,
        colorprimary = args.colorprimary,
        colorsecondary = args.colorsecondary,
        colortertiary = args.colortertiary,
        coloreyes = args.coloreyes,
        mother_id = args.mother_id,
        mother_fancy = args.mother_fancy,
        mother_exclusive = args.mother_exclusive,
        father_id = args.father_id,
        father_fancy = args.father_fancy,
        father_exclusive = args.father_exclusive,
        start_price = args.start_price,
        end_price = args.end_price,
        current_price = args.current_price,
        auction_type = args.auction_type,
        auction_start = args.auction_start,
        auction_end = args.auction_end,
        auction_duration = args.auction_duration
    )
    session.add(kitty)
    session.commit()
    logger.info("%s added to database", args.name)

if __name__ == '__main__':

    tmp_date = datetime(2019, 6, 8, 3, 53, 11)

    # Add parsers for both creating a database and adding a kitty
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create", description="Create database")
    sb_create.add_argument("--engine_string", default='sqlite:///../data/kitties.db',
                           help="SQLAlchemy connection URI for database")
    sb_create.set_defaults(func=create_db)

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--id", default=0, help="id of kitty")
    sb_ingest.add_argument("--name", default="OG", help="name of kitty")
    sb_ingest.add_argument("--image", default="https://img.cryptokitties.co/0x06012c8cf97bead5deae237070f9587f8e7a266d/1.png", help="image url for kitty")
    sb_ingest.add_argument("--generation", default=0, help="generation of kitty")
    sb_ingest.add_argument("--birthday", default=tmp_date, help="birthdate of kitty")
    sb_ingest.add_argument("--color", default="gold", help="main color of kitty")
    sb_ingest.add_argument("--fancy", default=True, help="fancy status of kitty")
    sb_ingest.add_argument("--exclusive", default=True, help="exclusive status of kitty")
    sb_ingest.add_argument("--fancy_type", default="TheFanciest", help="fancy type of kitty")
    sb_ingest.add_argument("--cooldown", default=11, help="cooldown index of kitty")
    sb_ingest.add_argument("--purrs", default=7, help="# of purrs for kitty")
    sb_ingest.add_argument("--watches", default=3, help="# of watches for kitty")
    # sb_ingest.add_argument("--hatched", default=False, help="hatch status of kitty")
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
    sb_ingest.add_argument("--auction_start", default=tmp_date, help="auction start for kitty")
    sb_ingest.add_argument("--auction_end", default=tmp_date, help="auction end for kitty")
    sb_ingest.add_argument("--auction_duration", default=1111111, help="auction duration for kitty")
    sb_ingest.add_argument("--auction_type", default="sale", help="auction type (sale or sire) for kitty")
    sb_ingest.add_argument("--engine_string", default='sqlite:///../data/kitties.db',
                           help="SQLAlchemy connection URI for database")
    sb_ingest.set_defaults(func=add_kitty)

    args = parser.parse_args()
    args.func(args)
