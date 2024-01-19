import pandas as pd
import numpy as np

#Define helper functions to generate dataframe for each graph


#function to get all the data
def get_all_data():
    df = pd.read_csv("C:\\Hinal\\Mini_project\\dashboard\\EIA data.csv")
    return df

#Function to get weekwise analysis data
def get_weekwise_data(commodity, num_years):
    df = get_all_data()
    df = df[::-1] #sorting data
    df['date'] = pd.to_datetime(df['date'])
    df['week_no'] = df['date'].dt.isocalendar().week
    df['year'] = df['date'].dt.year

    if num_years is None:
        num_years=5
    else:
        num_years = int(num_years)

    if(num_years==5):
        df = df[df['year'] >= 2019] #default-last 5 years data
    elif(num_years==10):
        df = df[df['year']>=2014]
    elif(num_years==15):
        df = df[df['year']>=2009]

    df.rename(columns={commodity:'stk'}, inplace=True)
    return df[['week_no', 'year', 'stk']]


#Function to get monthwise avg analysis data
def get_monthwise_data(commodity, num_years):
    df = get_all_data()
    df = df[::-1] #sorting data
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    temp = df.groupby(['year','month']).agg({commodity: 'mean'}).reset_index()

    if num_years is None:
        num_years=5
    else:
        num_years = int(num_years)

    if(num_years==5):
        temp = temp[temp['year'] >= 2019] #default-last 5 years data
    elif(num_years==10):
        temp = temp[temp['year']>=2014]
    elif(num_years==15):
        temp = temp[temp['year']>=2009]

    temp.rename(columns={commodity:'stk'}, inplace=True)
    return temp[['month', 'year', 'stk']]


def get_timewise_data(from_dt, to_dt):
    df = get_all_data()
    df['date'] = pd.to_datetime(df['date'])
    temp = df[(df['date'] >= pd.to_datetime(from_dt)) & (df['date'] <= pd.to_datetime(to_dt))]
    return temp
