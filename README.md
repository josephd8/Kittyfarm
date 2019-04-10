# ICOspy

#### The first stop for ICO research.

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

To assist beginner cryptos in their ICO research. 

### Mission
ICOs can be an intriguing investment option, but building up the knowledge (and possibly courage) to participate can be difficult. ICOspy aims to be a first stop for beginners looking to research ICO's. The goal of ICOspy is to provide a list of current Pre-ICOs ranked by promise. Doing so will help beginners know which ICO's to begin researching further.

### Success criteria

**Machine Learning**: It would be incredibly difficult to predict an actual 6-month forward looking sell price for a Pre-ICO. Instead, ICOspy will predict the Pre-ICO's future "Due Diligence Score" (DDS) as defined by Zloadr. In short, this is a score that has been given to ICO's as a measure of how well they have performed relative to one another. By predicting the future DDS for Pre-ICO's, ICOspy can then rank Pre-ICO's by their score. ICOspy is most interested in ranking Pre-ICO's as accurately as possible, rather than predicting their actual scores. This is because ICOspy aims to be a pre-research tool to build confidence as a beginner moves into ICO research. ICOspy's main value is providing confidence to the beginner that the ICO's they are moving to research are great places to start. Thus, ICOspy will use Mean Average Precision (MAP) to assess how precisely it ranks the top 10 Pre-ICO's. Whereas a MAP of 1 would be perfect, ICOspy will seek to achieve a MAP of .7. 

**Value Prop**: As time moves on, Pre-ICO's will go live and become live ICO's and new Pre-ICO's will appear. ICOspy will dynamically capture these changes and become even smarter at ranking Pre-ICO's. ICOspy will measure it's actual value by assessing the number of rankings generated, as well as the number of rankings exported (either via email or SMS). Again, ICOspy delivers value as new people come to start their ICOspy research, or as users return to re-generate new rankings to dive back into research.

#### Epics
* API - Assessment of features/data available from the Zloadr API on both Pre-ICO's and ICO's.
* Data - Development of dynamic (with time) training, testing, and validation datasets.
* Model - Development of supervised prediction models to rank Pre-ICO's by promise.
* App - Implementation of App to deliver Pre-ICO rankings with speed, efficiency, and ease.

#### Backlog
* (API) - establish API connection via Python (1)
* (API) - make initial calls to query for sample data (0)
* (API) - determine strategy to call for all needed data without exceeding API limits (2)
* (API) - write script to query all needed data that can be used dynamically through time (4)
* (Data) - build sample training, testing, and prediction sets from query results (2)
* (Model) - exploratory data analysis to aid in Feature Engineering (1)
* (App) - set up Flask app environment (4)
* (Data) - write script that will build datasets dynamically through time (4)
* (Model) - develop CV approach to test methods against MAP (2)
* (Model) - build Random Forest Model to predict Pre-Ico DDS (2)
* (Model) - build Gradient-Boosted Tree to predict Pre-Ico DDS (2)
* (App) - develop UI to generate rankings (4)
* (Model) - test models in CV (4)
* (Model) - productionize final models (4)
* (App) - develop functionality to export results via email or SMS (4)

#### Icebox
* (App) - develop UI to show basic info/summaries on Pre-ICO’s in rankings
* (App) - add summary info on the ICO market as a whole
* (API) - supplement data with pricing data on ICO’s from a different API (in order to stay below API limits)
* (Model) - explore ranking algorithms rather than prediction algorithms which will then be ranked



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
