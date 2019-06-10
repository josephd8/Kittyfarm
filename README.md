# Kittyfarm

## A (Crypto)Kitty value predictor

Developer: JD Cook
QA: Jonathan Lewyckyj

<!-- toc -->

- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Running the application](#running-the-application)
  - [Fetch data via CryptoKitties API](#fetch-data-via-api)
    - [Apply for Cryptokitty API credentials](#apply-for-credentials)
    - [Set API Token in Environmental Variables](#set-api-token)
    - [Configure AWS command line tools](#configure-aws)
    - [Configure AWS Access ID & Key](#configure-aws-access)
  - [Set up environment](#1-set-up-environment)
    - [With `virtualenv` and `pip`](#with-virtualenv-and-pip)
    - [With `conda`](#with-conda)
  - [Configure Flask app](#2-configure-flask-app)
  - [Initialize the database](#3-initialize-the-database)
  - [Land Kitties in s3 into database](#4-land-kitties)
  - [Train the model to predict kitty price](#5-train-model)
  - [Score a kitty](#6-score-kitty)
  - [Run the application](#7-run-the-application)
- [Testing](#testing)
- [Moving to EC2 (Production)](#production)

<!-- tocstop -->

## Project Charter

### Vision

Cryptokitties is a blockchain-based game that allows players to purchase, collent, breed, and sell virtual cats.

Kittyfarm will live assist beginner CryptoKitties owners in building their kitty "farm". (https://www.cryptokitties.co/)

### Mission

Kitty owners have an opportunity to build the value of their litter through breeding, but what breeding decisions are most likely to introduce valuable mutatuions and gene sets, thus increasing the litter value?

Kittyfarm will give owners the ability to simulate the breeding of two cats and view the probabilities of given genes. Kitty farm will also take those gene probabilities to infer an "expected value" of the new baby kitten. These core functionalities of Kittyfarm will help kitty owners make the right tradeoffs between cost of breeding and potential value increases through breeding.

### Success criteria

**Machine Learning**: The supervised models will be tasked with taking a mother cat and a sire (father) and essentially predicting the genome of the baby kitten. Predicting kitten genomes will enable Kittyfarm to show the traits that a kitten is most likely to inherit. Utilitizing 400k+ breeding instances, Kittyfarm will test the accuracy of models based on % of correct Cattributes (as they are called.) A relative service, CryptoBreeder.net, claims to achieve 94% accuracy in this metric. Thus, Kittyfarm will seek to achieve a correct Cattribute prediction rate of 95%.

And Kittyfarm will not stop there! With the probabilities of genes from a simulated breed, Kitty farm will create every possibility of baby kitten that could be created with those possible genes. Then, Kittyfarm will cross-check those potential kittens against the data itself to derive expected values, which will be weighted by likelihood and then aggregated to provide an overall expected value of the new baby kitten.

**Business**: Kittyfarm aims to provide real value to owners by helping them turn their breeding decisions into Ether (the cryptocurrency that powers CryptoKitties). From a usage perspective, the target metrics are 100 new users per month, 50% of users make a re-visit, and 1000 simulations generated per month. From a monetary perspective, Kittyfarm can assess real value by how willing users are to donate Ether in the form of tips to my Ether wallet. The monetary target metric is .061 Ether/month (currently $10 USD).

#### Themes

* Data as Engine - Focus on real-time, accurate, clean data as the engine
* Valuable Predictions - Generate valuable, actionable predictions/insight 
* Top-Tier UX - Provide top-tier user experience

#### Epics

* (Data as Engine) API - Assessment of features/data available from the CryptoKitties API.
* (Data as Engine) Data - Development of dynamic (with time) training, testing, and validation datasets.
* (Data as Engine, Valuable Predictions) Model - Development of supervised prediction models to predict a baby kitten's price.
* (Top-Tier UX) App - Implementation of App to enable user to input kitty id and generate prediction.

#### Backlog

* (API) - configure Kittyverse developer account and Kittyfarm Dapp. (1) - COMPLETE
* (API) - establish API connection via Python (1) - COMPLETE
* (API) - make initial calls to query for sample data (0) - COMPLETE
* (Data) - determine all needed data from CryptoKitties API (2) - COMPLETE
* (Data) - model data for RDS (4) - COMPLETE
* (API) - write script to query all needed data that can be used dynamically through time (4) - PLANNED
* (Data) - build sample training, testing, and validation sets from query results (2) - PLANNED
* (Data) - configure RDS instance to store data sets (2) - COMPLETE
* (Data) - explore the need for S3 instance to relay data from API to RDS (1) - COMPLETE
* (App) - set up Flask app environment (4) - COMPLETE
* (Model) - exploratory data analysis to aid in Feature Engineering (1) - COMPLETE
* (Data) - write script that will build datasets dynamically through time (4) - COMPLETE
* (Model) - explore potential models for price prediction (8) - COMPLETE
* (Model) - develop CV approach to test methods (2) - COMPLETE
* (App) - develop UI to input Kitty id (4) - COMPLETE
* (Model) - test models in CV (4) - COMPLETE
* (Model) - productionize final models (4) - COMPLETE
* (App) - develop functionality to export results via email or SMS (4) - BACKLOG

#### Icebox

* (App) - develop UI to show basic info/summaries on a Kitty in question. - BACKLOG
* (App) - add summary info on the Kittyverse as a whole. - BACKLOG
* (Model) - explore clustering algorithm to identify Kitties that should be priced in the same range, and then single out Kitties that are not priced similarly - BACKLOG

<!--Check out the the rest of the [Project Charter](charter.md) to see the metrics and backlog driving Kittyfarm!-->

This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Running the application

### Set up environment

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. See bottom of README for exploratory data analysis environment setup. 

#### With `virtualenv`

```bash
pip install virtualenv --user

virtualenv kitty

source kitty/bin/activate

pip install -r requirements.txt
conda install scikit-learn

```

#### With `conda`

```bash
conda create -n kitty python=3.7
conda activate kitty
pip install -r requirements.txt
conda install scikit-learn

```

### Fetching Kitty Data via API

#### Apply for Cryptokitty API credentials

Sign up for Cryptokitty API Access here: https://docs.api.cryptokitties.co/view/4668563/RWTrPGvN/?version=latest

After filling out the typeform, you will have to wait for them to email you your api token. They claim that this normally takes ~2-3 days.

#### Set API Token in Environmental Variables

Set your API Token as an environmental variable that the fetch_data.py script will use. Use the "Token" given to you by Cryptokitties, not the "Auth Token".

```bash
export KITTY_TOKEN=insert_api_token_here
```

#### Configure AWS command line tools

Create an access key: In the AWS console, go to "My Security Credentials" under your
username in the top right corner. Press `Create Access Key`. Save
your AWS Access Key ID and AWS Secret Access Key .

Configure aws command line tools in order to load files directly to S3 bucket.
python

```bash
pip install awscli --upgrade
aws configure
```

Follow the prompt to enter your aws key, aws secret, and aws region. This will allow automatic access to write and read from your S3 bucket.

Finally, set the S3 bucket name as an environmental variable:

```bash
export KITTY_BUCKET=insert_bucket_name_here
```

#### Configure AWS Access ID & Key

In order to interact with the public s3 bucket, you will need to set your AWS Access ID and AWS Access Key as environmental variables.

```bash
export AWS_ACCESS_ID=aws_access_id_here
export AWS_ACCESS_KEY=aws_access_key_here
```

#### Run fetch_sample_data.py script

The Cryptokitties data is updated as kittie's attributes changed - so calling the API at any time will give you up-to-date kitty info. Thus, there are no time parameters to the API call. In fact, because we are calling the "getKitties" endpoint, the only parameters are `limit` and `offset`, which can be reset within the fetch_sample_data.py script if you would like to get a larger or different sample. 

```bash
python src/fetch_sample_data.py
```

You should see successful logging messages as the sample data is called and put into your S3 bucket. The sample is a json file with data for 1000 kitties. 

It should be noted that the fetch_data.py script will work though a series of calls, each grabbing 5000 kitties at a time, until it has landed each kitties data into the S3 bucket (~1.6 million kitties, ~200 .json files, ~6.5 gb).

### Configure Flask app

`config/flask_config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
import os

ENV = "dev"

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "kittyfarm"
MODEL_CONFIG = "config/model_config.yml"
PATH_TO_MODEL = "models/kitties_model.pkl"
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "127.0.0.1"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

if(ENV == "dev"):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/kitties.db'
    HOME_ENGINE_STRING = 'sqlite:///data/kitties.db'
else:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:{}@kittyrds.caso2ns6uz08.us-east-2.rds.amazonaws.com:3306/kittyDB'.format(os.environ["RDS_PASSWORD"])
    HOME_ENGINE_STRING = 'mysql+pymysql://root:{}@kittyrds.caso2ns6uz08.us-east-2.rds.amazonaws.com:3306/kittyDB'.format(os.environ["RDS_PASSWORD"])

```

### Initialize the database

To create the database in the location configured in `config/flask_config.py` with one initial kitty, run:

```bash
python run.py create
```

### Land Kitties in s3 into database

To parse all of the kitties data out of the json files and into the database, run:

```bash
python run.py land
```

### Train the model to predict kitty price

To train a model using the parameters in `config/model_config.yml`, run:

```bash
python run.py train
```

### Score a kitty

To score (predict) a kitty based of the newly trained model, run:

```bash
python run.py score --kitty_id=1500000
```

### Run the application

Finally, to run the full application, run:

```bash
python run.py app
```

### Interact with the application

Go to [http://127.0.0.1:3000/]( http://127.0.0.1:3000/) to interact with the current version of the app.

## Testing

Run `pytest` from the command line in the main project repository.

Tests exist in `test/test_helpers.py`

## Moving to EC2

In order to deploy on EC2 using RDS as a database, the following settings must be changed in `config/flask_config.py`:

```python
ENV = "prod"
HOST = "0.0.0.0"
```

You could then follow all of the same instructions.

