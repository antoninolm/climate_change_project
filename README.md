# Predicting climate change effect over temperatures in France

## Project structure
/api : contains the API logic
/interface : contains the logic relative to the Streamlit UI
/ml_logic : contains all the machine learning logic from data cleaning to saving the model as a pickle file
/models : ignored in git, where the models are saved as pickle files
/notebooks : contains all the notebooks created
/raw_data : contains the raw data files of the datasets used for this project

## Getting started

1) Install packages in order to run the project with the command :

```
make install
```

2) Run the following command in order to create, train and save locally the model :

```
make train_and_save_model
```

## Running the project locally

```
make develop
```

## API

API related logic is located in the /api folder.
To run the API (V1), simply enter the following command in your terminal:

```
make run_api
```

## Front-end

Display a Streamlit webapp that makes uses of the API by running the following command :

```
make run_frontend
```
