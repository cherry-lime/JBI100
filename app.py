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
from plotly_calplot import calplot

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__)#, external_stylesheets=[dbc.themes.CYBORG])
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 
app.title = "JBI100 Dashboard"


if __name__ == '__main__':
    # Create data
    pd.options.mode.chained_assignment = None
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
                  #title='Traffic accidents in the UK in 2015',
                  template="plotly_dark",
                  width=1000, height=600),
        'Day of the week': px.scatter_mapbox(day_sorted, lat="Latitude", lon="Longitude", color="Accident_Severity",
                  #color_continuous_scale=px.colors.cyclical.IceFire, 
                  #size='Accident_Severity',
                  size_max=5, zoom=5,
                  hover_data=['Date','Time'],
                  mapbox_style="carto-positron",
                  animation_frame="Day_of_week",
                  template="plotly_dark",
                  #title='Traffic accidents in the UK in 2015'
                  ),
        'Hour': px.scatter_mapbox(hour_sorted, lat="Latitude", lon="Longitude", color="Accident_Severity",
                  #color_continuous_scale=px.colors.cyclical.IceFire, 
                  #size='Accident_Severity',
                  size_max=5, zoom=5,
                  hover_data=['Date','Time'],
                  mapbox_style="carto-positron",
                  animation_frame="Hour",
                  template="plotly_dark",
                  #title='Traffic accidents in the UK in 2015'
                  )
    }

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
                    html.Br(),
                    html.P("Select an animation:"),
                    dcc.RadioItems(
                        id='selection',
                        options=[{'label': x, 'value': x} for x in animations],
                        value='Month'
                    ),
                    dcc.Graph(id="gis-graph"),
                ], className="five columns"),

                html.Div([
                    html.H3('Sunburst graph'),
                    dcc.Graph(id="sunburst-graph")
                ], className="four columns")
            ]),

            html.Div([                
                
                html.Div([
                    html.H3('Histogram'),
                    dcc.Graph(id="histo-graph")
                ], className="five columns"),

                html.Div([
                    html.H3('Boxplot'),
                    dcc.Graph(id="box-plot"),
                ], className="four columns"),
                
                ]
            ),

            html.Div([
                html.H3("Cal plot"),
                dcc.Graph(id="cal-plot"),
            ], className="six columns"
            ),
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

    @app.callback(
        Output("sunburst-graph","figure"),
        [Input("sunburstmenu","value")]
    )
    def update_sunburstgraph(sunburstmenu):
        fig = px.sunburst(df_sunburst, path=sunburstmenu,
                template="plotly_dark",
                width=500, height=500
                )
        return fig

    @app.callback(
        Output("box-plot","figure"),
        [Input("boxmenu","value")]
    )
    def update_boxplt(boxmenu):
        fig = px.violin(road_clean, y=boxmenu, box=True,
                color='cluster',
                points='all', # can be 'outliers', or False
                template="plotly_dark",
               )
        return fig

    @app.callback(
        Output("cal-plot", "figure"),
        [Input("boxmenu", "value")]
    )
    def update_calplot(boxmenu):
        fig = calplot(road_clean, x = "Datetime", y=boxmenu, dark_theme=True,)
        return fig
    app.run_server(debug=False, dev_tools_ui=False)