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

app = dash.Dash(__name__)#, external_stylesheets=[dbc.themes.CYBORG])
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
                html.H1(children="Dashboard"),
            ),


            html.Div(
                #id="left-column",
                #className="dash-bootstrap",
                children=[#make_menu_layout(),
                    #dcc.Dropdown(
                    #    id=
                    #)
                    
                    dcc.Graph(id="sunburst-graph",figure=fig),
                    dcc.Dropdown(
                        id="dropdown1",
                        options=[{"label":x,"value":x} for x in road_clean.columns],
                        value=road_clean.columns[11],
                        clearable=False
                    ),
                    dcc.Dropdown(
                        id="dropdown2",
                        options=[{"label":x,"value":x} for x in road_clean.columns],
                        value=road_clean.columns[10],
                        clearable=False,
                        className="dropdown"
                    ),
                    #dbc.DropdownMenu(
                    #    label="Choose the value for y",
                    #    color="Secondary",
                    #    menu_variant="dark",
                    #    children=[x for x in road_clean.columns],
                    #    id="dropdown3"
                    #),
                    dcc.Graph(id="histo-graph")
                
                ],
            ),
    
            # Right column
            html.Div(
                #id="right-column",
                #className="right-column",
                children=[
                    #scatterplot1,
                    #scatterplot2
                    #html.H1('Heading', style={'backgroundColor':'blue'}),
                    html.P("Select an animation:"),
                    dcc.RadioItems(
                        id='selection',
                        options=[{'label': x, 'value': x} for x in animations],
                        value='Month'
                    ),
                    dcc.Graph(id="gis-graph"),
                ],
                

            ),
        ],
    )

    # Define interactions
#    @app.callback(
#        Output(scatterplot1.html_id, "figure"), [
#        Input("select-color-scatter-1", "value"),
#        Input(scatterplot2.html_id, 'selectedData')
#    ])
#    def update_scatter_1(selected_color, selected_data):
#        return scatterplot1.update(selected_color, selected_data)

#    @app.callback(
#        Output(scatterplot2.html_id, "figure"), [
#        Input("select-color-scatter-2", "value"),
#        Input(scatterplot1.html_id, 'selectedData')
#    ])
#    def update_scatter_2(selected_color, selected_data):
#        return scatterplot2.update(selected_color, selected_data)

    @app.callback(
        Output("gis-graph","figure"),
        [Input("selection","value")])
    
    def display_animated_graphs(s):
        return animations[s]

    #@app.callback(
    #    Output("sunburst-graph", "figure"),
        
    #)
    #def display_sunburst_graph():
    #    fig = px.sunburst(df_sunburst, path=['Sex_of_Driver', 'Age_of_Driver'],
    #                title='Driver sex and age distribution'
    #                )
    #    return fig
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