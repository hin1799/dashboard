from django.http import JsonResponse
import pandas as pd
from rest_framework.response import Response
from rest_framework import status
from .serializers import DataSerializer, WeekwiseDataSerializer, MonthwiseDataSerializer, WeekWiseDifferenceDataSerializer, SummerDataSerializer, AggDataWeekMonthSerializer
from rest_framework.decorators import api_view
from .helpers import get_all_data, get_weekwise_data, get_monthwise_data, get_weekwise_difference, get_summer_data, get_aggregate_analysis_weekly

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

    
#Average, min, max, 2023 analysis
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
    
    return Response(serializer.data)


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