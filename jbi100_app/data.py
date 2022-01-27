import pandas as pd
import numpy as np # linear algebra

def get_data():
    # Read data
    df = pd.read_csv('jbi100_app/data/dataset.csv')

    # Any further data preprocessing can go here
    df = df.replace('?', np.nan)
    roads = df.drop(columns=['Junction_Control', '2nd_Road_Class','Age_of_Vehicle','Engine_Capacity_(CC)','Propulsion_Code','Driver_Home_Area_Type'])
    roads = roads.dropna()
    intermediate = roads.drop(columns=['Accident_Index','Location_Easting_OSGR','Location_Northing_OSGR','Longitude','Latitude','Date','Time','Local_Authority_(Highway)','LSOA_of_Accident_Location'])
    intermediate = intermediate.astype('int64')
    intermediate2 = roads[['Accident_Index','Location_Easting_OSGR','Location_Northing_OSGR','Longitude','Latitude','Date','Time','Local_Authority_(Highway)','LSOA_of_Accident_Location']]
    road_clean = intermediate2.join(intermediate)
    road_clean['Longitude'] = road_clean['Longitude'].astype('float64')
    road_clean['Latitude'] = road_clean['Latitude'].astype('float64')
    road_clean['Year']=road_clean['Accident_Index'].str[:4]
    road_clean['Month']=road_clean['Date'].str[3:5]

    return road_clean
