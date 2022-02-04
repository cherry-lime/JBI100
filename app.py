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
    df_box = get_data()[4]
    
    # Instantiate custom views
    animations = {
        'Month': road_clean,

        'Day of the week': day_sorted,

        'Hour': hour_sorted
    }
    # Overall layout
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
                    html.H5("Select an animation:"),
                    dcc.Graph(id="cartograph"),
                ], className="five columns"),

                html.Div([
                    html.H5('Sunburst graph'),
                    dcc.Graph(id="sunburst-graph")
                ], className="four columns")
            ]),

            html.Div([                
                
                html.Div([
                    html.H5('Histogram'),
                    dcc.Graph(id="histo-graph")
                ], className="five columns"),

                html.Div([
                    html.H5('Boxplot'),
                    dcc.Graph(id="box-plot"),
                ], className="four columns"),
                
                ]
            ),

            html.Div([
                html.H5("Cal plot"),
                dcc.Graph(id="cal-plot"),
            ], className="six columns"
            ),
        ],
    )

    # Interaction features 
    # Histogram
    @app.callback(
        Output("histo-graph","figure"),
        [Input("dropdown1","value")],
        [Input("dropdown2","value")]
    )
    def update_histograph(dropdown1, dropdown2):

        fig = px.histogram(road_clean, x=dropdown1, 
                            color=dropdown2,template="plotly_dark",
                            width=1000, height=500)
        return fig

    # Sunburst graph
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

    # Map
    @app.callback(
        Output("cartograph","figure"),
        [Input("boxmenu","value")],
        [Input("timerange","value")],
        [Input("colormode","value")]
    )

    def update_map(boxmenu, timerange, colormode):
        if colormode == 'discrete':
            road_clean[boxmenu] = road_clean[boxmenu].astype(str)
        else:
            road_clean[boxmenu] = road_clean[boxmenu].astype(float)
        if timerange == "Month":
            fig = px.scatter_mapbox(road_clean, lat="Latitude", lon="Longitude", color=boxmenu,
                #color_continuous_scale=px.colors.cyclical.IceFire, 
                #size='Accident_Severity',
                size_max=5, zoom=5,
                hover_data=['Date','Time'],
                mapbox_style="carto-positron",
                animation_frame="Month",
                template="plotly_dark",
                #title='Traffic accidents in the UK in 2015'
                )
        elif timerange == "Day of the week":
            fig = px.scatter_mapbox(day_sorted, lat="Latitude", lon="Longitude", color=boxmenu,
                #color_continuous_scale=px.colors.cyclical.IceFire, 
                #size='Accident_Severity',
                size_max=5, zoom=5,
                hover_data=['Date','Time'],
                mapbox_style="carto-positron",
                animation_frame="Day_of_week",
                template="plotly_dark",
                #title='Traffic accidents in the UK in 2015'
                )
        elif timerange == "Hour":
            fig = px.scatter_mapbox(hour_sorted, lat="Latitude", lon="Longitude", color=boxmenu,
                #color_continuous_scale=px.colors.cyclical.IceFire, 
                #size='Accident_Severity',
                size_max=5, zoom=5,
                hover_data=['Date','Time'],
                mapbox_style="carto-positron",
                animation_frame="Hour",
                template="plotly_dark",
                #title='Traffic accidents in the UK in 2015'
                )
        else: print("Incorrect input.")
        fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest', dragmode='lasso',)
        return fig

    # Box plot
    @app.callback(
        Output("box-plot","figure"),
        [Input("boxmenu","value")]
    )
    def update_boxplt(boxmenu):
        fig = px.violin(df_box, y=boxmenu, box=True,
                color='cluster',
                points='all', # can be 'outliers', or False
                template="plotly_dark",
               )
        return fig

    @app.callback(
        Output("cal-plot", "figure"),
        [Input("boxmenu", "value")]
    )

    # Calendar plot
    def update_calplot(boxmenu):
        fig = calplot(road_clean, x = "Datetime", y=boxmenu, dark_theme=True,)
        return fig
    app.run_server(debug=False, dev_tools_ui=False)