# Predicting climate change effect over temperatures in France

## Project structure
/api : contains the API logic
/interface : contains the logic relative to the Streamlit UI
/ml_logic : contains all the machine learning logic from data cleaning to saving the model as a pickle file
/models : ignored in git, where the models are saved as pickle files
/notebooks : contains all the notebooks created
/raw_data : contains the raw data files of the datasets used for this project

## Getting started

Install packages in order to run the project with the command :

```
make setup
```

## Running the project locally

```
make develop
```

## API

API related logic is located in the /api folder.
To run the API (V1), simply enter the following command in your terminal:

```
fastapi run api/main.py
```

## Front-end

Display a Streamlit webapp that makes uses of the API by running the following command :

```
streamlit run interface/frontend.py
```
