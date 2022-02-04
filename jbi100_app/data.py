import numpy as np 
import pandas as pd

def get_data():
    # Read data
    pd.options.mode.chained_assignment = None  # default='warn'
    road = pd.read_csv("dataset.csv")
    clustered = pd.read_csv("kmeans.csv", index_col=0)
    # Data cleaning
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
    df_sunburst = road_clean.copy()
    df_sunburst['Sex_of_Driver']=df_sunburst['Sex_of_Driver'].replace(1, 'Men')
    df_sunburst['Sex_of_Driver']=df_sunburst['Sex_of_Driver'].replace(2, 'Women')
    df_sunburst['Sex_of_Driver']=df_sunburst['Sex_of_Driver'].replace(3, 'Unknown')
    road_clean['cluster']=clustered['kmeans cluster']
    return road_clean, day_sorted, hour_sorted, df_sunburst
