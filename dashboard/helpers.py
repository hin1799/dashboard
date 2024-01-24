import pandas as pd
import numpy as np


#function to get all the data
def get_all_data():
    df = pd.read_csv("C:\\Hinal\\Mini_project\\dashboard\\EIA data.csv")
    return df

def get_dataframe():
    df = get_all_data()
    df = df[::-1] #sorting data
    df['date'] = pd.to_datetime(df['date'])
    df['week_no'] = df['date'].dt.isocalendar().week
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    return df


def filter_df_yearwise(df, num_years):
    if num_years is None:
        num_years=5
    else:
        num_years = int(num_years)

    if(num_years==1):
        df = df[df['year'] >= 2023]
    elif(num_years==2):
        df = df[df['year'] >= 2022]
    elif(num_years==5):
        df = df[df['year'] >= 2019] #default-last 5 years data
    elif(num_years==10):
        df = df[df['year']>=2014]
    elif(num_years==15):
        df = df[df['year']>=2009]
    
    return df

#Function to get weekwise analysis data
def get_weekwise_data(commodity, num_years):
    df = get_dataframe()
    df = filter_df_yearwise(df, num_years)

    df.rename(columns={commodity:'stk'}, inplace=True)
    return df[['week_no', 'year', 'stk']]

#Function to get monthwise avg analysis data
def get_monthwise_data(commodity, num_years):
    df = get_dataframe()
    temp = df.groupby(['year','month']).agg({commodity: 'mean'}).reset_index()
    temp = filter_df_yearwise(temp, num_years)
    temp.rename(columns={commodity:'stk'}, inplace=True)
    return temp[['month', 'year', 'stk']]

def get_percentage_data(num_years):
    df = get_dataframe()
    df = filter_df_yearwise(df, num_years)

    #Calculating the percentage
    df['spr_per'] = (df['crude_stk_spr']/df['crude_stk'])*100
    df['gas_per'] = (df['gas_stk']/df['crude_stk'])*100
    df['dist_per'] = (df['dist_stk']/df['crude_stk'])*100

    return df[['date', 'spr_per', 'gas_per', 'dist_per']]

def get_percentage_data_yearly():
    df = get_dataframe()
    df['spr_per'] = (df['crude_stk_spr']/df['crude_stk'])*100
    df['gas_per'] = (df['gas_stk']/df['crude_stk'])*100
    df['dist_per'] = (df['dist_stk']/df['crude_stk'])*100

    df_per_year = df.groupby('year').agg({'spr_per': 'mean', 'gas_per': 'mean', 'dist_per':'mean'})

    df_per_year = df_per_year.reset_index()
    return df_per_year[['year', 'spr_per', 'gas_per', 'dist_per']]

#Function to get the weekwise difference data
def get_weekwise_difference(commodity, num_years):
    df = get_dataframe()
    df_week = df.copy()
    df_week['week_diff'] = df_week['week_no'].astype(str).shift(1) + '-' + df_week['week_no'].astype(str)
    df_week['stk'] = df_week[commodity].shift(1) - df_week[commodity]
    df_week = filter_df_yearwise(df_week, num_years)
    return df_week[['week_diff', 'year', 'stk']]


#Function to get the average stocks in summer months
def get_summer_data(commodity, num_years):
    df = get_dataframe()
    df_summer = df[df['month'].isin([5,6,7,8])]
    df_summer = df_summer.groupby(['year','month']).agg({commodity:'mean', 'date':'first'})
    df_summer = df_summer.reset_index()
    df_summer = filter_df_yearwise(df_summer, num_years)
    df_summer.rename(columns={commodity:'stk'}, inplace=True)
    return df_summer[['date', 'stk']]

def get_aggregate_analysis_weekly(commodity):
    df = get_dataframe()
    df1 = df.copy()
    df1_dump_2023_CRUDE = list(df1[df1['year']==2023][commodity])
    df1_dump_CRUDE = df1[df1['week_no']!= 53][df1['year'] != 2023].groupby('week_no').agg({commodity:['mean', 'min', 'max']})
    df1_dump_CRUDE['2023'] = df1_dump_2023_CRUDE
    df1_dump_CRUDE = df1_dump_CRUDE.reset_index()
    df1_dump_CRUDE.columns = ['week_month', 'avg', 'minimum', 'maximum','data_2023']
    return df1_dump_CRUDE

def get_aggregate_analysis_monthly(commodity):
    df = get_dataframe()
    df1 = df.copy()
    df1_dump_2023_CRUDE_Monthly = df1[df1['year']==2023].groupby('month').agg({commodity: 'mean'}).values
    df2_dump_CRUDE = df1[df1['year'] != 2023].groupby('month').agg({commodity:['mean', 'min', 'max']})
    df2_dump_CRUDE['2023'] = df1_dump_2023_CRUDE_Monthly
    df2_dump_CRUDE = df2_dump_CRUDE.reset_index()
    df2_dump_CRUDE.columns = ['week_month', 'avg', 'minimum', 'maximum','data_2023']
    return df2_dump_CRUDE

def monthwise_build_draw(commodity, from_month, to_month):
    df = get_dataframe()
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

    if from_month > to_month:
        df_diff = pd.concat(
        [df4[(df4['month']==months[from_month])].groupby(['year']).agg({commodity:'min'}).shift(),
        df4[(df4['month']==months[to_month])].groupby(['year']).agg({commodity:'max'})],
        axis=1)
    else:
        df_diff = pd.concat(
        [df4[(df4['month']==months[from_month])].groupby(['year']).agg({commodity:'min'}),
        df4[(df4['month']==months[to_month])].groupby(['year']).agg({commodity:'max'})],
        axis=1)

    
    df_diff.columns = ['From Month', 'To Month']
    df_diff['diff'] = (- df_diff['From Month'] + df_diff['To Month'])
    print(df_diff)
    df_diff = df_diff.reset_index()

    df_diff['build_or_draw'] = df_diff['diff'].apply(lambda x: 'b' if x > 0 else 'd')
    
    df_diff = df_diff.dropna(axis=0)
    df_diff.columns = ['year', 'curr_month_stk', 'prev_month_stk', 'diff', 'build_or_draw']
    return df_diff[['year', 'curr_month_stk', 'prev_month_stk', 'build_or_draw']]

def build_draw_yearly(commodity, num_years):
    df = get_dataframe()
    temp = df.copy()
    temp = filter_df_yearwise(temp, num_years)
    temp['diff'] = temp[commodity].diff()
    temp = temp.reset_index()
    temp.rename(columns={commodity:'stk'}, inplace=True)
    temp = temp.drop(0)
    return temp[['date', 'stk', 'diff']]

def build_draw_percentage(commodity):
    df = get_dataframe()

    df['inventory_diff'] = df[commodity].diff()
    df['build_draw'] = df['inventory_diff'].apply(lambda x: -1 if x<0 else 1)

    pivot_table = df.pivot_table(index='month', columns='build_draw', aggfunc='size')
    pivot_table['total'] = pivot_table.sum(axis=1)
    pivot_table['build_per'] = (pivot_table[1]/pivot_table['total'])*100
    pivot_table['draw_per'] = (pivot_table[-1]/pivot_table['total'])*100

    pivot_table = pivot_table.reset_index()
    return pivot_table[['month','build_per','draw_per']]

def build_draw_percentage_weekly(commodity):
    df = get_dataframe()

    df['inventory_diff'] = df[commodity].diff()
    df['build_draw'] = df['inventory_diff'].apply(lambda x: -1 if x<0 else 1)

    pivot_table_week = df.pivot_table(index='week_no', columns='build_draw', aggfunc='size')
    pivot_table_week['total'] = pivot_table_week.sum(axis=1)
    pivot_table_week['build_per'] = (pivot_table_week[1]/pivot_table_week['total'])*100
    pivot_table_week['draw_per'] = (pivot_table_week[-1]/pivot_table_week['total'])*100

    pivot_table = pivot_table_week.reset_index()
    pivot_table.rename(columns={'week_no':'week'}, inplace=True)
    pivot_table.drop(pivot_table.tail(1).index, inplace=True)
    pivot_table = pivot_table.fillna(0)

    return pivot_table[['week', 'build_per', 'draw_per']]

def build_draw_heatmap(commodity):
    df = get_dataframe()

    df['inventory_diff'] = df[commodity].diff()
    df['build_draw'] = df['inventory_diff'].apply(lambda x: -1 if x<0 else 1)

    df_heatmap = df.groupby(['month', 'year']).agg({commodity: 'mean', 'build_draw': 'sum'})
    df_heatmap = df_heatmap.reset_index()

    return df_heatmap[['month', 'year', 'build_draw']]

def inventory_diff_heatmap(commodity):
    df = get_dataframe()

    df['inventory_diff'] = df[commodity].diff()
    df['build_draw'] = df['inventory_diff'].apply(lambda x: -1 if x<0 else 1)

    df_heatmap = df.groupby(['month', 'year']).agg({'inventory_diff': 'mean', 'build_draw':'sum'})
    df_heatmap = df_heatmap.reset_index()

    return df_heatmap[['month', 'year', 'inventory_diff']]


#Function to get data in a particular timeframe
def get_timewise_data(from_dt, to_dt):
    df = get_all_data()
    df['date'] = pd.to_datetime(df['date'])
    temp = df[(df['date'] >= pd.to_datetime(from_dt)) & (df['date'] <= pd.to_datetime(to_dt))]
    return temp
