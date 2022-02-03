from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
import numpy as np 
import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.io as pio
from jbi100_app.data import get_data

pd.options.mode.chained_assignment = None  # default='warn'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__)#, external_stylesheets=[dbc.themes.CYBORG])
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 
app.title = "JBI100 Dashboard"


if __name__ == '__main__':
    # Create data
    road_clean = get_data()[0]
    day_sorted = get_data()[1]
    hour_sorted = get_data()[2]
    df_sunburst = get_data()[3]

    # Instantiate custom views
    animations = {
        'Month': px.scatter_mapbox(road_clean, lat="Latitude", lon="Longitude", color="Accident_Severity",
                  #color_continuous_scale=px.colors.cyclical.IceFire, 
                  size_max=5, zoom=5,
                  hover_data=['Date','Time'],
                  mapbox_style="carto-positron",
                  animation_frame="Month",
                  title='Traffic accidents in the UK in 2015',
                  template="plotly_dark",
                  width=800, height=600),
        'Day of the week': px.scatter_mapbox(day_sorted, lat="Latitude", lon="Longitude", color="Accident_Severity",
                  #color_continuous_scale=px.colors.cyclical.IceFire, 
                  #size='Accident_Severity',
                  size_max=5, zoom=5,
                  hover_data=['Date','Time'],
                  mapbox_style="carto-positron",
                  animation_frame="Day_of_week",
                  template="plotly_dark",
                  title='Traffic accidents in the UK in 2015'),
        'Hour': px.scatter_mapbox(hour_sorted, lat="Latitude", lon="Longitude", color="Accident_Severity",
                  #color_continuous_scale=px.colors.cyclical.IceFire, 
                  #size='Accident_Severity',
                  size_max=5, zoom=5,
                  hover_data=['Date','Time'],
                  mapbox_style="carto-positron",
                  animation_frame="Hour",
                  template="plotly_dark",
                  title='Traffic accidents in the UK in 2015')
    }


    fig = px.sunburst(df_sunburst, path=['Sex_of_Driver', 'Age_of_Driver'],
                    title='Driver sex and age distribution',
                    template="plotly_dark",
                    width=500, height=500
                    )

    app.layout = html.Div(
        id="app-container",
        children=[
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout()
            ),
            html.Div([
                html.Div([
                    html.H3('Interactive histogram'),
                    dcc.Graph(id="histo-graph")
                ], className="six columns"),

                html.Div([
                    html.H3('Sunburst graph'),
                    dcc.Graph(id="sunburst-graph",figure=fig)
                ], className="six columns")
            ], className="container"),
            html.Div([
                html.Div([
                    html.P("Select an animation:"),
                    dcc.RadioItems(
                        id='selection',
                        options=[{'label': x, 'value': x} for x in animations],
                        value='Month'
                    ),
                    dcc.Graph(id="gis-graph"),
                ], className="six columns")
            ], className="container")
        ],
    )

    @app.callback(
        Output("gis-graph","figure"),
        [Input("selection","value")])
    
    def display_animated_graphs(s):
        return animations[s]

    @app.callback(
        Output("histo-graph","figure"),
        [Input("dropdown1","value")],
        [Input("dropdown2","value")]
    )
    def update_histograph(dropdown1, dropdown2):

        fig = px.histogram(road_clean, x=dropdown1, 
                            color=dropdown2,template="plotly_dark",
                            width=800, height=500)
        return fig
        
    app.run_server(debug=False, dev_tools_ui=False)