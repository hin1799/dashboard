from django.http import JsonResponse
import pandas as pd
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .helpers import build_draw_percentage, get_all_data, get_percentage_data, get_percentage_data_yearly, get_weekwise_data, get_monthwise_data, get_weekwise_difference, get_summer_data, get_aggregate_analysis_weekly, get_aggregate_analysis_monthly, monthwise_build_draw, build_draw_yearly
from .serializers import *
from .modify_json import *

@api_view(['GET'])
def raw_chart_basic(request, format=None):
    '''Raw plot- Function to get all the EIA data'''
    df = get_all_data()
    df = df[::-1]
    data = df.to_dict(orient='records')
    serializer = DataSerializer(data, many=True)
    return Response(serializer.data)

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
    json = json_for_weekwise_raw(serializer.data)
    return Response(json)
   


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
    json = json_for_monthwise_raw(serializer.data)
    return Response(json)


@api_view(['GET'])
def raw_chart_percentage(request, format=None):
    '''Raw plot - Function to plot the percentage wise distribution of gas, spr and distillates from the crude oil stocks'''
    num_years = request.GET.get('years') #optional parameter - default=5
    df = get_percentage_data(num_years)
    data = df.to_dict(orient='records')
    serializer = PercentageDataSerializer(data, many=True)
    json = json_for_percentage_data(serializer.data)
    return Response(json)

@api_view(['GET'])
def raw_chart_percentage_yearly(request, format=None):
    '''Raw plot - Function to plot the percentage wise distribution of gas, spr and distillates from the crude oil stocks'''
    df = get_percentage_data_yearly()
    data = df.to_dict(orient='records')
    serializer = PercentageYearlySerializer(data, many=True)
    json = json_for_percentage_data_yearly(serializer.data)
    return Response(json)
    

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
    json = json_for_weekwise_difference(serializer.data)
    return Response(json)

    

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
    json = json_for_summer_analysis(serializer.data)
    return Response(json)
    


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
    json = json_for_weekwise_aggregation(serializer.data)
    return Response(json)
    


@api_view(['GET'])
def simple_chart_monthwise_aggregations(request, format=None):
    '''Simple plot - Function to plot the monthly average, minimim and maximum of 2004-2021 vs 2023 data'''

    commodity = request.GET.get('commodity') 

    if commodity is None:
        return Response(status=status.HTTP_400_BAD_REQUEST) 
    
    df = get_aggregate_analysis_monthly(commodity)
    data = df.to_dict(orient='records')
    serializer = AggDataWeekMonthSerializer(data, many=True)
    json = json_for_monthwise_aggregation(serializer.data)
    return Response(json)


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
    json = json_for_build_draw_monthwise(serializer.data)
    return Response(json)


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
    json = json_for_build_draw_years(serializer.data)
    return Response(json)


@api_view(['GET'])
def advanced_chart_build_draw_percentage(request, format=None):
    '''Advanced plot - Function to show the build and draw percentage in each month over the years'''
    commodity = request.GET.get('commodity')

    df = build_draw_percentage(commodity)
    data = df.to_dict(orient='records')
    serializer = BuildDrawPercentageSerializer(data, many=True)
    json = json_for_build_draw_percentage(serializer.data)
    return Response(json)





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