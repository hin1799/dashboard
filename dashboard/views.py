from django.http import JsonResponse
import pandas as pd
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .helpers import build_draw_percentage, get_all_data, get_weekwise_data, get_monthwise_data, get_weekwise_difference, get_summer_data, get_aggregate_analysis_weekly, get_aggregate_analysis_monthly, monthwise_build_draw, build_draw_yearly
from .serializers import *

#API for raw plot to show initially on dashboard - /raw/
@api_view(['GET'])
def raw_chart_basic(request, format=None):
    '''Raw plot- Function to get all the EIA data'''
    df = get_all_data()
    data = df.to_dict(orient='records')
    serializer = DataSerializer(data, many=True)
    return Response(serializer.data)

#API for weekwise analysis - /raw/weekwise/?commmodity={commodity}&years={num_years}
@api_view(['GET'])
def raw_chart_weekwise(request, format=None):
    '''Raw plot - Function to get weekwise analysis data'''

    #select commodity - required query parameter
    commodity = request.GET.get('commodity')
    num_years = request.GET.get('years') #optional parameter - number of years data

    if commodity is None:
        return Response(status=status.HTTP_400_BAD_REQUEST) 

    df = get_weekwise_data(commodity, num_years) #default=5 years data
    data = df.to_dict(orient='records')
    serializer = WeekwiseDataSerializer(data, many=True)

    converted_data = {}

    converted_data = {"week_no": set(), "year": {}}

    for entry in serializer.data:
        week = entry["week_no"]
        year = entry["year"]
        stk = entry["stk"]

        converted_data["week_no"].add(week)

        if year not in converted_data["year"]:
            converted_data["year"][year] = []

        converted_data["year"][year].append(stk)

    # return Response(serializer.data)
    return Response(converted_data)


#API for monthwise analysis - /raw/monthwise/?commmodity={commodity}&years={num_years}
@api_view(['GET'])
def raw_chart_monthwise(request, format=None):
    '''Raw plot - Function to get monthwise avg analysis data'''

    #select commodity - required query parameter
    commodity = request.GET.get('commodity')
    num_years = request.GET.get('years') #optional parameter - number of years data

    if commodity is None:
        return Response(status=status.HTTP_400_BAD_REQUEST) 

    df = get_monthwise_data(commodity, num_years) #default=5 years data
    data = df.to_dict(orient='records')
    serializer = MonthwiseDataSerializer(data, many=True)
    converted_data = {}

    converted_data = {"month": set(), "year": {}}

    for entry in serializer.data:
        month = entry["month"]
        year = entry["year"]
        stk = entry["stk"]

        converted_data["month"].add(month)

        if year not in converted_data["year"]:
            converted_data["year"][year] = []

        converted_data["year"][year].append(stk)

    # return Response(serializer.data)
    return Response(converted_data)


#API for simple analysis - /simple/weekwise_diff/?commodity={commodity}&years={num_years}
@api_view(['GET'])
def simple_chart_weekwise_diff(request, format=None):
    '''Simple plot - Function to get weekwise difference of stocks data'''

    commodity = request.GET.get('commodity')
    num_years = request.GET.get('years')

    if commodity is None:
        return Response(status=status.HTTP_400_BAD_REQUEST) 

    df = get_weekwise_difference(commodity, num_years) #default=5 years data
    data = df.to_dict(orient='records')
    serializer = WeekWiseDifferenceDataSerializer(data, many=True)

    #Update json
    converted_data = {}

    converted_data = {"week_diff": set(), "year": {}}

    for entry in serializer.data:
        week_diff = entry["week_diff"]
        year = entry["year"]
        stk = entry["stk"]

        converted_data["week_diff"].add(week_diff)

        if year not in converted_data["year"]:
            converted_data["year"][year] = []

        converted_data["year"][year].append(stk)

    return Response(converted_data)

#API for simple analysis - /simple/summer_analysis/?commodity={commodity}&years={num_years}
@api_view(['GET'])
def simple_chart_summer_analysis(request, format=None):
    '''Simple plot - Function to plot the avg monthly stocks in summer months'''
    
    commodity = request.GET.get('commodity')
    num_years = request.GET.get('years')

    if commodity is None:
        return Response(status=status.HTTP_400_BAD_REQUEST) 

    df = get_summer_data(commodity, num_years) #default=5 years data
    data = df.to_dict(orient='records')
    serializer = SummerDataSerializer(data, many=True)

    converted_data = {"date": [], "stk": []}

    for entry in serializer.data:
        date_str = entry["date"]
        stk = entry["stk"]

        converted_data["date"].append(date_str)
        converted_data["stk"].append(stk)

    return Response(converted_data)

    
#Average, min, max, 2023 analysis weekwise
@api_view(['GET'])
def simple_chart_weekwise_aggregations(request, format=None):
    '''Simple plot - Function to plot the weekly average, minimim and maximum of 2004-2021 vs 2023 data'''

    commodity = request.GET.get('commodity') 
    print("commodity", commodity)
    if commodity is None:
        return Response(status=status.HTTP_400_BAD_REQUEST) 
    
    df = get_aggregate_analysis_weekly(commodity)
    data = df.to_dict(orient='records')
    serializer = AggDataWeekMonthSerializer(data, many=True)

    #Update json
    converted_data = {"week": [], "data": {"avg": [], "min":[], "max":[], "yr2023":[]}}

    for entry in serializer.data:
        week = entry["week_month"]
        avg = entry["avg"]
        min = entry["minimum"]
        max = entry["maximum"]
        yr2023 = entry["data_2023"]

        converted_data["week"].append(week)
        converted_data["data"]["avg"].append(avg)
        converted_data["data"]["min"].append(min)
        converted_data["data"]["max"].append(max)
        converted_data["data"]["yr2023"].append(yr2023)

    return Response(converted_data)

#Average, min, max, 2023 analysis
@api_view(['GET'])
def simple_chart_monthwise_aggregations(request, format=None):
    '''Simple plot - Function to plot the monthly average, minimim and maximum of 2004-2021 vs 2023 data'''

    commodity = request.GET.get('commodity') 

    if commodity is None:
        return Response(status=status.HTTP_400_BAD_REQUEST) 
    
    df = get_aggregate_analysis_monthly(commodity)
    data = df.to_dict(orient='records')
    serializer = AggDataWeekMonthSerializer(data, many=True)

    #Update json
    converted_data = {"month": [], "data": {"avg": [], "min": [], "max": [], "yr2023": []}}

    for entry in serializer.data:
        month = entry["week_month"]
        avg = entry["avg"]
        min = entry["minimum"]
        max = entry["maximum"]
        yr2023 = entry["data_2023"]

        converted_data["month"].append(month)
        converted_data["data"]["avg"].append(avg)
        converted_data["data"]["min"].append(min)
        converted_data["data"]["max"].append(max)
        converted_data["data"]["yr2023"].append(yr2023)

    return Response(converted_data)


#Advanced chart - monthwise comparisons
@api_view(['GET'])
def advanced_chart_build_draw_curr_prev_month(request, format=None):
    '''Advanced plot - Function to plot the difference in stocks in 2 given months and show it as build or draw'''

    commodity = request.GET.get('commodity') 
    curr_month = request.GET.get('curr')
    prev_month = request.GET.get('prev')

    if commodity is None or curr_month is None or prev_month is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    df = monthwise_build_draw(commodity, curr_month, prev_month)
    data = df.to_dict(orient='records')
    serializer = MonthwiseBuildDrawSerializer(data, many=True)

    #update json
    converted_data = {"year": [], "data": {"curr_month_stk": [], "prev_month_stk": [], "build_or_draw": []}}

    for entry in serializer.data:
        year = entry["year"]
        curr = entry["curr_month_stk"]
        prev = entry["prev_month_stk"]
        build_draw = entry["build_or_draw"]

        converted_data["year"].append(year)
        converted_data["data"]["curr_month_stk"].append(curr)
        converted_data["data"]["prev_month_stk"].append(prev)
        converted_data["data"]["build_or_draw"].append(build_draw)

    return Response(converted_data)

#Advanced chart - amount of build and draw (line+bar chart)
@api_view(['GET'])
def advanced_chart_build_draw_years(request, format=None):
    '''Advanced plot - Function to show the build or draw over weeks and also the amount of build and draw'''
    commodity = request.GET.get('commodity')
    num_years = request.GET.get('years')

    if commodity is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    df = build_draw_yearly(commodity, num_years)
    data = df.to_dict(orient='records')
    serializer = YearwiseBuildDrawSerializer(data, many=True)

    #update json
    converted_data = {"date": [], "data": {"stk": [], "diff": []}}

    for entry in serializer.data:
        date = entry["date"]
        stk = entry["stk"]
        diff = entry["diff"]

        converted_data["date"].append(date)
        converted_data["data"]["stk"].append(stk)
        converted_data["data"]["diff"].append(diff)

    return Response(converted_data)

#Advanced chart on build draw percentage analysis
@api_view(['GET'])
def advanced_chart_build_draw_percentage(request, format=None):
    '''Advanced plot - Function to show the build and draw percentage in each month over the years'''
    commodity = request.GET.get('commodity')

    df = build_draw_percentage(commodity)
    data = df.to_dict(orient='records')
    serializer = BuildDrawPercentageSerializer(data, many=True)

    #modify json
    converted_data = {"month": [], "data": {"build_per": [], "draw_per": []}}

    for entry in serializer.data:
        month = entry["month"]
        build_per = entry["build_per"]
        draw_per = entry["draw_per"]

        converted_data["month"].append(month)
        converted_data["data"]["build_per"].append(build_per)
        converted_data["data"]["draw_per"].append(draw_per)

    return Response(converted_data)

#api-> /data/
# @api_view(['GET'])
# def getdata(request, format=None):
#     '''Function to get all the EIA data'''

#     from_dt = request.GET.get('from')
#     to_dt = request.GET.get('to')

#     #if query params are passed:
#     if from_dt and to_dt:
#         df = get_timewise_data(from_dt, to_dt)
#     #return all data
#     else:
#         df = get_all_data()
#     data = df.to_dict(orient='records')
#     serializer = DataSerializer(data, many=True)
#     return Response(serializer.data)