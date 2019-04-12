# Kittyfarm

#### A (Crypto)Kitty gene & value predictor.

<!-- toc -->

- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Documentation](#documentation)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `virtualenv` and `pip`](#with-virtualenv-and-pip)
    + [With `conda`](#with-conda)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Initialize the database](#3-initialize-the-database)
  * [4. Run the application](#4-run-the-application)
- [Testing](#testing)

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
* (Data as Engine, Valuable Predictions) Model - Development of supervised prediction models to predict a baby kitten's genome.
* (Top-Tier UX) App - Implementation of App to enable user to input gene set and generate prediction.

#### Backlog
* (API) - configure Kittyverse developer account and Kittyfarm Dapp. (1) - PLANNED
* (API) - establish API connection via Python (1) - PLANNED
* (API) - make initial calls to query for sample data (0) - PLANNED
* (Data) - determine all needed data from CryptoKitties API (2) - PLANNED
* (Data) - model data for RDS (4) - PLANNED
* (API) - write script to query all needed data that can be used dynamically through time (4) - PLANNED
* (Data) - build sample training, testing, and validation sets from query results (2) - PLANNED
* (Data) - configure RDS instance to store data sets (2) - PLANNED
* (Data) - explore the need for S3 instance to relay data from API to RDS (1) - PLANNED
* (App) - set up Flask app environment (4) - PLANNED
* (Model) - exploratory data analysis to aid in Feature Engineering (1) - PLANNED
* (Data) - write script that will build datasets dynamically through time (4) - PLANNED
* (Model) - explore potential models for genome prediction (8)
* (Model) - develop CV approach to test methods (2) 
* (App) - develop UI to input Kitty gene set (4)
* (Model) - test models in CV (4)
* (Model) - productionize final models (4)
* (App) - develop functionality to export results via email or SMS (4)

#### Icebox
* (App) - develop UI to show basic info/summaries on a Kitty in question.
* (App) - add summary info on the Kittyverse as a whole.
* (Model) - explore clustering algorithm to identify Kitties that should be priced in the same range, and then single out Kitties that are not priced similarly

<!--Check out the the rest of the [Project Charter](charter.md) to see the metrics and backlog driving Kittyfarm!-->

## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── models.py                     <- Creates the data model for the database connected to the Flask app 
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── archive/                      <- Place to put archive data is no longer usabled. Not synced with git. 
│   ├── external/                     <- External data sources, will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures                           <- Generated graphics and figures to be used in reporting.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│   ├── archive                       <- No longer current models. This directory is included in the .gitignore and is not tracked by git
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports and helper functions. 
│
├── src                               <- Source data for the project 
│   ├── archive/                      <- No longer current scripts.
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── sql/                          <- SQL source code
│   ├── add_songs.py                  <- Script for creating a (temporary) MySQL database and adding songs to it 
│   ├── ingest_data.py                <- Script for ingesting data from different sources 
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── train_model.py                <- Script for training machine learning model(s)
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── postprocess.py                <- Script for postprocessing predictions and model results
│   ├── evaluate_model.py             <- Script for evaluating model performance 
│
├── test                              <- Files necessary for running model tests (see documentation below) 

├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── app.py                            <- Flask wrapper for running the model 
├── config.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).


# TO BE EDITED LATER

## Documentation
 
* Open up `docs/build/html/index.html` to see Sphinx documentation docs. 
* See `docs/README.md` for keeping docs up to date with additions to the repository.

## Running the application 
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. See bottom of README for exploratory data analysis environment setup. 

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv pennylane

source pennylane/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n pennylane python=3.7
conda activate pennylane
pip install -r requirements.txt

```

### 2. Configure Flask app 

`config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
PORT = 3002  # What port to expose app on 
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tracks.db'  # URI for database that contains tracks

```


### 3. Initialize the database 

To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

To add additional songs:

`python run.py ingest --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`


### 4. Run the application 
 
 ```bash
 python app.py 
 ```

### 5. Interact with the application 

Go to [http://127.0.0.1:3000/]( http://127.0.0.1:3000/) to interact with the current version of hte app. 

## Testing 

Run `pytest` from the command line in the main project repository. 


Tests exist in `test/test_helpers.py`
