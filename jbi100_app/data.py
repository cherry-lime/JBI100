import pandas as pd

def get_data():
    # Read data
    df = pd.read_csv('data/dataset.csv')

    # Any further data preprocessing can go here

    return df
