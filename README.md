# Milestone3_Churn_WebApp

## About this project

This project takes the churn prediction model from an earlier notebook and turns it into something usable — a simple form where you enter a customer's details and get back a prediction along with a probability score. No need to open a notebook or run any code, just fill in the numbers and hit run.

It's meant to simulate how a retention team might actually use a model like this day to day: quickly check a customer's risk level and decide whether to step in before they cancel.

## How it works

You enter nine details about a customer — things like subscription age, average bill, remaining contract length, and download/upload usage. Behind the scenes, the app calculates a few extra features from those inputs (the same ones the model was trained on, like usage ratios and a loyalty flag) and feeds all of it into a trained Random Forest model. The model returns a prediction - likely to churn or likely to stay - plus a probability percentage.

Every prediction gets logged to a file so there's a record of what was checked and when.

## Model performance

- Algorithm: Random Forest
- Accuracy: 93.81%
- F1 Score: 94%

The model was compared against Logistic Regression and a Decision Tree during development, and Random Forest came out ahead on both accuracy and consistency.

## Project structure

Milestone3_Churn_WebApp/

├── app.py → Flask app and prediction logic

├── model.pkl → trained Random Forest model (tracked via Git LFS)

├── requirements.txt → Python dependencies

├── templates/

│ └── index.html → main page

├── static/

│ └── style.css → styling

└── logs/

└── app.log → prediction history


## Running it locally

1. Clone the repo

 git clone https://github.com/coding1035919-spec/Milestone3_Churn_WebApp.git
 
 cd Milestone3_Churn_WebApp

2. (Recommended) create and activate a virtual environment

python -m venv .venv
.venv\Scripts\activate

3. Install the dependencies
 pip install -r requirements.txt

4. Run the app
 python app.py


5. Open your browser and go to `http://127.0.0.1:5000`

## Note on the model file

`model.pkl` is tracked with Git LFS since it's on the larger side. If you clone this repo and the model doesn't load correctly, make sure you have [Git LFS](https://git-lfs.github.com) installed and run `git lfs pull` after cloning.

## What I'd improve next

- Add input validation on the frontend so obviously invalid values (like negative usage) get caught before hitting the model
- Try hyperparameter tuning to see if accuracy can be pushed further
- Deploy it somewhere public (Render or Railway) instead of just running locally

## Author

coding1035919-spec





