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
import dash_bootstrap_components as dbc

pd.options.mode.chained_assignment = None  # default='warn'

app = dash.Dash(__name__)#, external_stylesheets=[dbc.themes.CYBORG])
app.title = "JBI100 Dashboard"

if __name__ == '__main__':
    # Create data
    road = pd.read_csv("dataset.csv")
    road = road.replace('?', np.nan)
    roads = road.drop(columns=['Junction_Control', '2nd_Road_Class','Age_of_Vehicle','Engine_Capacity_(CC)','Propulsion_Code','Driver_Home_Area_Type'])
    roads = roads.dropna()
    intermediate = roads.drop(columns=['Accident_Index','Location_Easting_OSGR','Location_Northing_OSGR','Longitude','Latitude','Date','Time','Local_Authority_(Highway)','LSOA_of_Accident_Location'])
    intermediate = intermediate.astype('int64')
    intermediate2 = roads[['Accident_Index','Location_Easting_OSGR','Location_Northing_OSGR','Longitude','Latitude','Date','Time','Local_Authority_(Highway)','LSOA_of_Accident_Location']]
    road_clean = intermediate2.join(intermediate)
    road_clean = road_clean.dropna()
    road_clean['Longitude'] = road_clean['Longitude'].astype('float64')
    road_clean['Latitude'] = road_clean['Latitude'].astype('float64')
    road_clean['Year']=road_clean['Accident_Index'].str[:4]
    road_clean['Month']=road_clean['Date'].str[3:5]
    road_clean['Hour']=road_clean['Time'].str[:2]
    road_clean['Day']=road_clean['Date'].str[:2]
    road_clean = road_clean.dropna()
    road_clean['Year']=road_clean['Year'].astype('int64')
    road_clean['Month']=road_clean['Month'].astype('int64')
    road_clean['Hour']=road_clean['Hour'].astype('int64')
    road_clean['Day']=road_clean['Day'].astype('int64')
    road_clean['Datetime'] = road_clean['Date'].replace('/','-')
    road_clean['Datetime'] = pd.to_datetime(road_clean.Date)
    road_clean['Day_of_week']=road_clean['Datetime'].dt.dayofweek
    road_clean['Day_of_week']=road_clean['Day_of_week']+1
    day_sorted = road_clean.copy()
    hour_sorted = road_clean.copy()
    day_sorted.sort_values('Day_of_week', ascending=True, ignore_index=True, inplace=True)
    hour_sorted.sort_values('Hour', ascending=True, ignore_index=True, inplace=True)

    # For the sunburst graph
    df_sunburst = road_clean.copy()
    df_sunburst['Sex_of_Driver']=df_sunburst['Sex_of_Driver'].replace(1, 'Men')
    df_sunburst['Sex_of_Driver']=df_sunburst['Sex_of_Driver'].replace(2, 'Women')
    df_sunburst['Sex_of_Driver']=df_sunburst['Sex_of_Driver'].replace(3, 'Unknown')
    #df_sunburst['Age_group']=df_sunburst['Age_of_Driver'].mask(df_sunburst['Age_of_Driver'] < 18, 'Under 18')
    #df_sunburst['Age_group']=df_sunburst['Age_group'].mask(df_sunburst['Age_of_Driver'] >= 60, 'Over 60')
    #df_sunburst['Age_group']=np.where(df_sunburst['Age_of_Driver'].between(18,29), '18 to 29', df_sunburst['Age_group'])
    #df_sunburst['Age_group']=np.where(df_sunburst['Age_of_Driver'].between(30,39), '30 to 39', df_sunburst['Age_group'])
    #df_sunburst['Age_group']=np.where(df_sunburst['Age_of_Driver'].between(40,49), '40 to 49', df_sunburst['Age_group'])
    #df_sunburst['Age_group']=np.where(df_sunburst['Age_of_Driver'].between(50,59), '50 to 59', df_sunburst['Age_group'])
 

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