import plotly.express as px


def get_data():
    # Read data
    df = px.data.iris()

    # Any further data preprocessing can go here

    return df
