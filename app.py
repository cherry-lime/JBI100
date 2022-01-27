from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.data import get_data
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


if __name__ == '__main__':
    # Create data
    df = get_data()

    # Instantiate custom views
    scatterplot1 = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="Accident_Severity",
                  #color_continuous_scale=px.colors.cyclical.IceFire, 
                  size_max=3, zoom=5,
                  hover_data=['Date','Time'],
                  mapbox_style="carto-positron",
                  animation_frame="Month",
                  title='Traffic accidents in the UK in 2015')
    scatterplot1.update_traces(marker_size=3, opacity=0.5)                  

    scatterplot2 = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="Sex_of_Driver",
                  #color_continuous_scale=px.colors.cyclical.IceFire, 
                  size='Accident_Severity',
                  size_max=8, zoom=5,
                  hover_data=['Date','Time'],
                  mapbox_style="carto-positron",
                  animation_frame="Month",
                  title='Traffic accidents in the UK in 2015')
    scatterplot2.update_traces(marker_size=3, opacity=0.5)                  

    heatmap = px.density_mapbox(df, lat='Latitude', lon='Longitude', z="Accident_Severity", radius=3,
                        #center=dict(lat=0, lon=180), 
                        zoom=5,
                        mapbox_style="stamen-terrain",
                        animation_frame="Month",
                        title='Traffic accidents in the UK in 2015')

    app.layout = html.Div(children=[
        # All elements from the top of the page
        html.Div([
            html.H1(children='Hello Dash'),

            html.Div(children='''
                Dash: A web application framework for Python.
            '''),

            dcc.Graph(
                id='scatterplot1',
                figure=scatterplot1
            ),  
        ]),
        # New Div for all elements in the new 'row' of the page
        html.Div([ 
            dcc.Graph(
                id='scatterplot2',
                figure = scatterplot2
            ),
            html.Label([
                "colorscale",
                dcc.Dropdown(
                    id='colorscale-dropdown', clearable=False,
                    value='bluyl', options=[
                        {'label': c, 'value': c}
                        for c in px.colors.named_colorscales()
                    ])
            ]),
        ]),
        html.Div([ 
            dcc.Graph(
                id='heatmap',
                figure = heatmap
            ),
        ])
    ])

    # Callback function that automatically updates the tip-graph based on chosen colorscale
    @app.callback(
        Output('scatterplot2', 'figure'),
        [Input("colorscale-dropdown", "value")]
    )
    def update_scatterplot(colorscale):
        return px.scatter_mapbox(
            df, lat="Latitude", lon="Longitude", color="Accident_Severity",
            colorscale=px.colors.cyclical.IceFire, 
            size_max=3, zoom=5,
            hover_data=['Date','Time'],
            mapbox_style="carto-positron",
            animation_frame="Month",
            title='Traffic accidents in the UK in 2015',
            render_mode="webgl"
        )


    app.run_server(debug=False, dev_tools_ui=False)