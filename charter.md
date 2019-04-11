## Project Charter 

### Vision

To assist beginner CryptoKitties owners in building their kitty farm. 

### Mission
Cryptokitties is a blockchain-based game that allows players to purchase, collect, breed, and sell virtual cats. While some people play purely for the novelty of discovering new mutations (appropriately named "mewtations") and breeding a pool of their very own kitties, others play CryptoKitties in an effort to earn money by making breeding decisions that produce a kitty that is more valuable than the input needed to breed. Whatever the reason, Kittyfarm will help new entrants to CryptoKitties by providing a predicted value for a kitty with any given gene set. 

### Success criteria

**Machine Learning**: The supervised models will be tasked with predicting a kitty's price (value) at any point and time. These prices fluctuate depending on the kitty market. Kittyfarm will use RMSE to evaluate models in their ability to correctly predict price. An RMSE of 2 ($2 USD) is the beginning line in the sand. This will likely need adjusted as Kittyfarm progresses as it may be more accurate for lower priced kitties (because there are so many), and less accurate for high-end (outlier) kitties.

**Value Prop**: Kittyfarm's value lies in its ability to give new users a feel for what gene's and combinations are most valuable in CryptoKitties. It will also give users a platform to help with their breeding decisions as they try and assess which genes are most important to bring into their farm. Kittyfarm seeks to help any beginner CryptoKitties owner to find more joy in their litter, and also more value in their kitty farm. As a whole, # of unique users, # of re-visits, and # of predictions generated are the main metrics that signal whether Kittyfarm is delivering this value.

#### Themes
* Focus on real-time, accurate, clean data as the engine
* Generate valuable, actionable predictions/insight 
* Provide top-tier user experience

#### Epics
* (Data as Engine) API - Assessment of features/data available from the CryptoKitties API.
* (Data as Engine) Data - Development of dynamic (with time) training, testing, and validation datasets.
* (Data as Engine, Valuable Predictions) Model - Development of supervised prediction models to predict a kitty's price based on it's gene set.
* (Top-Tier UX) App - Implementation of App to enable user to input gene set and generate prediction.

#### Backlog
* (API) - configure Kittyverse developer account and Kittyfarm Dapp. (1) 
* (API) - establish API connection via Python (1)
* (API) - make initial calls to query for sample data (0)
* (API) - determine strategy to call for all needed data without exceeding API limits (2)
* (API) - write script to query all needed data that can be used dynamically through time (4)
* (Data) - build sample training, testing, and validation sets from query results (2)
* (Model) - exploratory data analysis to aid in Feature Engineering (1)
* (App) - set up Flask app environment (4)
* (Data) - write script that will build datasets dynamically through time (4)
* (Model) - develop CV approach to test methods against RMSE (2)
* (Model) - build Random Forest Model to predict Kitty price (2)
* (Model) - build Gradient-Boosted Tree to predict Kitty price (2)
* (Model) - build Neural-Network to predict Kitty price (2)
* (App) - develop UI to input Kitty gene set (4)
* (Model) - test models in CV (4)
* (Model) - productionize final models (4)
* (App) - develop functionality to export results via email or SMS (4)

#### Icebox
* (App) - develop UI to show basic info/summaries on a Kitty in question.
* (App) - add summary info on the Kittyverse as a whole.
* (Model) - explore clustering algorithm to identify Kitties that should be priced in the same range, and then single out Kitties that are not priced similarly
