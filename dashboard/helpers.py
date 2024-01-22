import pandas as pd
import numpy as np


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

#Function to get the weekwise difference data
def get_weekwise_difference(commodity, num_years):
    df = get_all_data()
    df = df[::-1] #sorting data
    df['date'] = pd.to_datetime(df['date'])
    df['week_no'] = df['date'].dt.isocalendar().week
    df['year'] = df['date'].dt.year

    df_week = df.copy()
    df_week['week_diff'] = df_week['week_no'].astype(str).shift(1) + '-' + df_week['week_no'].astype(str)
    df_week['stk'] = df_week[commodity].shift(1) - df_week[commodity]

    if num_years is None:
        num_years=5
    else:
        num_years = int(num_years)

    if(num_years==5):
        df_week = df_week[df_week['year'] >= 2019] #default-last 5 years data
    elif(num_years==10):
        df_week = df_week[df_week['year']>=2014]
    elif(num_years==15):
        df_week = df_week[df_week['year']>=2009]

    return df_week[['week_diff', 'year', 'stk']]


#Function to get the average stocks in summer months
def get_summer_data(commodity, num_years):
    df = get_all_data()
    df = df[::-1] #sorting data
    df['date'] = pd.to_datetime(df['date'])
    df['week_no'] = df['date'].dt.isocalendar().week
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    df_summer = df[df['month'].isin([5,6,7,8])]
    df_summer = df_summer.groupby(['year','month']).agg({commodity:'mean', 'date':'first'})
    df_summer = df_summer.reset_index()

    if num_years is None:
        num_years=5
    else:
        num_years = int(num_years)

    if(num_years==5):
        df_summer = df_summer[df_summer['year'] >= 2019] #default-last 5 years data
    elif(num_years==10):
        df_summer = df_summer[df_summer['year']>=2014]
    elif(num_years==15):
        df_summer = df_summer[df_summer['year']>=2009]
    
    df_summer.rename(columns={commodity:'stk'}, inplace=True)
    return df_summer[['date', 'stk']]

def get_aggregate_analysis_weekly(commodity):
    df = get_all_data()
    df = df[::-1] #sorting data
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.isocalendar().week
    df['year'] = df['date'].dt.year

    df1 = df.copy()

    df1_dump_2023_CRUDE = list(df1[df1['year']==2023][commodity])
    df1_dump_CRUDE = df1[df1['week']!= 53][df1['year'] != 2023].groupby('week').agg({commodity:['mean', 'min', 'max']})
    df1_dump_CRUDE['2023'] = df1_dump_2023_CRUDE
    
    df1_dump_CRUDE = df1_dump_CRUDE.reset_index()
    df1_dump_CRUDE.columns = ['week_month', 'avg', 'minimum', 'maximum','data_2023']

    return df1_dump_CRUDE

def get_aggregate_analysis_monthly(commodity):
    df = get_all_data()
    df = df[::-1] #sorting data
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.isocalendar().week
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    df1 = df.copy()

    df1_dump_2023_CRUDE_Monthly = df1[df1['year']==2023].groupby('month').agg({commodity: 'mean'}).values
    df2_dump_CRUDE = df1[df1['year'] != 2023].groupby('month').agg({commodity:['mean', 'min', 'max']})
    df2_dump_CRUDE['2023'] = df1_dump_2023_CRUDE_Monthly
    df2_dump_CRUDE = df2_dump_CRUDE.reset_index()
    df2_dump_CRUDE.columns = ['week_month', 'avg', 'minimum', 'maximum','data_2023']

    return df2_dump_CRUDE

def monthwise_build_draw(commodity, curr_month, prev_month):
    df = get_all_data()
    df = df[::-1] #sorting data
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.isocalendar().week
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df4 = df.copy()

    months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
    }

    df_diff = pd.concat([df4[(df4['month']==months[curr_month])].groupby(['year']).agg({commodity:'mean'}), df4[(df4['month']==months[prev_month])].groupby(['year']).agg({commodity:'mean'}).shift()], axis=1)
    df_diff.columns = ['Current Month', 'Previous Month']
    df_diff['diff'] = df_diff['Current Month'] - df_diff['Previous Month']
    df_diff['build_or_draw'] = df_diff['diff'].apply(lambda x: 'b' if x > 0 else 'd')
    df_diff = df_diff.drop('diff', axis=1)
    df_diff = df_diff.reset_index()
    df_diff = df_diff.drop(0)

    print(df_diff)

    df_diff.columns = ['year', 'curr_month_stk', 'prev_month_stk', 'build_or_draw']
    return df_diff
    
#Function to get data in a particular timeframe
def get_timewise_data(from_dt, to_dt):
    df = get_all_data()
    df['date'] = pd.to_datetime(df['date'])
    temp = df[(df['date'] >= pd.to_datetime(from_dt)) & (df['date'] <= pd.to_datetime(to_dt))]
    return temp
